from typing import List, Dict, Any, Generator

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
from .entities import IncomeByDateEntity
from .entities import IncomeByItemEntity
from .values import LabelValue

SCOPES = ['https://www.googleapis.com/auth/drive']
LOGGER = logging.getLogger(__name__)


def run():
        
    es_host = os.getenv('ES_HOST', ['localhost:9200'])
    service_account_file = os.getenv('SERVICE_ACCOUNT_FILE')
    upload_file_name = os.getenv(
        'UPLOAD_FILE_NAME',
        f'income-{str(datetime.now().year)}.csv')

    # Prepare credential
    LOGGER.info('Prepare credential.')
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)

    service = build('drive', 'v3', credentials=credentials)

    # Access drive
    LOGGER.info('Get file ids from drive.')
    results = service.files().list(\
        orderBy='modifiedTime desc',\
        q=f"name='{upload_file_name}'",\
        fields="nextPageToken, files(id, name, modifiedTime)").execute()

    LOGGER.info(dir(results))

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


# TODO conditional flow for lifeline usage
def construct_esdoc_by_date(msgs: List[Dict[Any]], index: str) -> Generator[Dict[Any], None, None]:
    for m in msgs:
        doc_id = md5(m['report_date'].encode('utf-8')).hexdigest()
        body = IncomeByDateEntity(updated_on=datetime.utcnow(), **m).dict()

        yield dict(_id=doc_id, _op_type='index', _index=index, **body)


def construct_esdoc_by_item(msgs: List[Dict[Any]], index: str) -> Generator[Dict[Any], None, None]:
    for m in msgs:
        keys = filter(lambda x: x != 'report_date', m.keys())

        for k in keys:
            item_label: list = LabelValue.__fields__[k].get_default()
            doc_id = md5(f"{m['report_date']}_{''.join(item_label)}_{k}".encode('utf-8'))\
                    .hexdigest()

            body = IncomeByItemEntity(
                    report_date=m['report_date'],
                    updated_on = datetime.utcnow(),
                    item_key=k,
                    item_value=m[k],
                    item_labels=item_label).dict()

            yield dict(_id=doc_id, _op_type='index', _index=index, **body)
