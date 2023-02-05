import csv
from typing import Dict, Any
import pytest


@pytest.fixture
def single_month_report_as_dict():
    with open('fixtures/report.csv') as csvfile:
        reader: csv.DictReader[Any] = csv.DictReader(csvfile)
        type_inferred: Dict[str, Any] = {}

        for row in reader:
            for k in row.keys():
                type_inferred[k] = int(row[k]) if k != 'report_date' else row[k]

        return [type_inferred]
