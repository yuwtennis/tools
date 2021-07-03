
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO, StringIO
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import csv
import logging
import json
import os
from hashlib import md5
from datetime import datetime

class Client:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.INFO)
    ES_INDEX = 'income'
    DATEFORMAT = '%Y-%m-%dT%H:%M:%SZ'

    @classmethod
    def run(cls):
        
        es_host = os.getenv('ES_HOST', ['localhost:19200'])
        service_account_file = os.getenv('SERVICE_ACCOUNT_FILE')

        # Prepare credential
        cls.LOGGER.info('Prepare credential.')
        credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=cls.SCOPES)

        service = build('drive', 'v3', credentials=credentials)

        # Access drive
        cls.LOGGER.info('Get file ids from drive.')
        results = service.files().list(\
            orderBy='modifiedTime desc',\
            q="name='income-2021.csv'",\
            fields="nextPageToken, files(id, name, modifiedTime)").execute()


        items = results.get('files', [])
        cls.LOGGER.info(items)

        request = service.files().get_media(fileId=items[0]['id'])

        fh = BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while done is False:
            status, done = downloader.next_chunk()
            cls.LOGGER.info("Download %d%%." % int(status.progress() * 100))

        # Write to elasticsearch
        cls.LOGGER.info('Send to elasticsearch.')
        fh = StringIO(fh.getvalue().decode(), newline='')

        bulk(
            Elasticsearch(hosts=es_host),
            cls._construct_esdoc(list(csv.DictReader(fh)), cls.ES_INDEX)
        )

    @classmethod
    def _construct_esdoc(cls, msgs, index):
        def conv_str_to_int(msgs):
            for msg in msgs:
                for k,v in msg.items():
                    if msg[k].isdigit():
                        msg[k] = int(v)

            return msgs

        now = datetime.utcnow()
        msgs = conv_str_to_int(msgs)

        for msg in msgs:
            doc_id = md5()
            doc_id.update(msg['report_date'].encode())
            msg.update({
                'updated_on': now.strftime(cls.DATEFORMAT),
                '_op_type': 'index',
                '_index': index,
                '_id': doc_id.hexdigest()})

            yield msg
