
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO, StringIO
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import csv
import logging
import os
from hashlib import md5
from datetime import datetime
from .schema import IncomeByDate
from .schema import IncomeByItem

SCOPES = ['https://www.googleapis.com/auth/drive']
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

def run():
        
    es_host = os.getenv('ES_HOST', ['localhost:19200'])
    service_account_file = os.getenv('SERVICE_ACCOUNT_FILE')

    # Prepare credential
    LOGGER.info('Prepare credential.')
    credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=SCOPES)

    service = build('drive', 'v3', credentials=credentials)

    # Access drive
    LOGGER.info('Get file ids from drive.')
    results = service.files().list(\
        orderBy='modifiedTime desc',\
        q="name='income-2021.csv'",\
        fields="nextPageToken, files(id, name, modifiedTime)").execute()


    items = results.get('files', [])
    LOGGER.info(items)

    request = service.files().get_media(fileId=items[0]['id'])

    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False

    while done is False:
        status, done = downloader.next_chunk()
        LOGGER.info("Download %d%%." % int(status.progress() * 100))

    # Write to elasticsearch
    LOGGER.info('Send to elasticsearch.')
    fh = StringIO(fh.getvalue().decode(), newline='')

    data = list(csv.DictReader(fh))
    es_inst = Elasticsearch(hosts=es_host)

    bulk(
        es_inst,
        construct_esdoc_by_date(
            data, 'income_by_date')
    )

    bulk(
            es_inst,
            construct_esdoc_by_item(
                data, 'income_by_item')
        )


def construct_esdoc_by_date(msgs, index):
    for m in msgs:
        doc_id = md5(m['report_date'].encode('utf-8')).hexdigest()
        body = IncomeByDate(updated_on=datetime.utcnow(), **m).dict()

        yield dict(_id=doc_id, _op_type='index', _index=index, **body)

def construct_esdoc_by_item(msgs, index):
    for m in msgs:
        keys = filter(lambda x: x != 'report_date', m.keys())

        for k in keys:
            doc_id = md5(f"{m['report_date']}_{m[k]}".encode('utf-8'))\
                    .hexdigest()

            body = IncomeByItem(
                    report_date=m['report_date'],
                    updated_on = datetime.utcnow(),
                    item_key=k,
                    item_value=m[k]).dict()

            yield dict(_id=doc_id, _op_type='index', _index=index, **body)
