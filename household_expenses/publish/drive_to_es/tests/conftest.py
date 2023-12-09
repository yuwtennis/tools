import csv
from pathlib import Path
from typing import Dict, Any
import pytest


PATH_TO_FIXTURE = f'{str(Path(__file__).resolve().parent.absolute())}/fixtures'


@pytest.fixture(scope="function")
def env(monkeypatch):
    monkeypatch.setenv("ES_HOST", "http://elasticsearch:9200")
    monkeypatch.setenv("SERVICE_ACCOUNT_INFO", '{"type":"service_account",' \
                         '"project_id":"my_project_id",' \
                         '"private_key_id":"abcdefgh",' \
                         '"private_key":"the_private_key",' \
                         '"client_email":"dev-xx@hoge.iam.gserviceaccount.com",' \
                         '"client_id":"106313935326358400493",' \
                         '"auth_uri":"https://accounts.google.com/o/oauth2/auth",' \
                         '"token_uri":"https://oauth2.googleapis.com/token",' \
                         '"auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",' \
                         '"client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/dev-xx%40hoge.iam.gserviceaccount.com"}')


@pytest.fixture(scope="function")
def single_month_report_as_dict():
    with open(f'{PATH_TO_FIXTURE}/report.csv') as csvfile:
        reader: csv.DictReader[Any] = csv.DictReader(csvfile)
        type_inferred: Dict[str, Any] = {}

        for row in reader:
            for k in row.keys():
                type_inferred[k] = int(row[k]) if k != 'report_date' else row[k]

        return [type_inferred]
