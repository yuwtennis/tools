from drive_to_es.client import construct_esdoc_by_date
from pathlib import Path
from typing import List, Any, Dict

PATH_TO_FIXTURE = f'{str(Path(__file__).resolve().parent.absolute())}/fixtures'


def test_construct_esdoc_by_date(single_month_report_as_dict):
    index_name: str = 'a_index'
    result: List[Dict[str, Any]] \
        = list(construct_esdoc_by_date(list(single_month_report_as_dict), index_name))

    for k, v in single_month_report_as_dict[0].items():
        assert result[0].get(k) == v


# TODO
#def test_construct_esdoc_by_item(single_month_report_as_dict):
