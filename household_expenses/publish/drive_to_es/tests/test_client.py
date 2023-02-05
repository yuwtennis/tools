from pathlib import Path
from typing import List, Any, Dict

import sys

from pkgs import values
from pkgs.values import LabelValue

sys.path.append(str(Path(__file__).resolve().parent.parent.absolute()))
from pkgs.client import construct_esdoc_by_date, construct_esdoc_by_item


def test_construct_esdoc_by_date(single_month_report_as_dict):
    index_name: str = 'a_index'
    result: List[Dict[str, Any]] \
        = list(construct_esdoc_by_date(list(single_month_report_as_dict), index_name))

    for k, v in single_month_report_as_dict[0].items():
        assert result[0].get(k) == v


# TODO
#def test_construct_esdoc_by_item(single_month_report_as_dict):
