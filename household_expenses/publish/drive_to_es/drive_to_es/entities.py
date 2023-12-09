""" Entity module """
from datetime import datetime
from typing import Any
from pydantic import BaseModel, AnyHttpUrl, Json, BaseSettings

# pylint: disable=too-few-public-methods


class Env(BaseSettings):
    """
    Attributes
    ----------
    es_host: http/https url for elasticsearch host
    service_account_info; A valid API Key for Service Account
    upload_file_name: The income statement csv file name
    """
    es_host: AnyHttpUrl
    service_account_info: Json[Any]  # pylint: disable=unsubscriptable-object
    upload_file_name: str = f'income-{str(datetime.now().year)}.csv'


class IncomeByDateEntity(BaseModel):
    """ Entity which holds income info by date """
    report_date: str
    updated_on: datetime
    income_tax: int = 0
    resident_tax: int = 0
    life_insurance: int = 0
    nursing_insurance: int = 0
    employment_insurance: int = 0
    health_insurance: int = 0
    welfare_pension: int = 0
    savings: int = 0
    securities: int = 0
    n401k: int = 0
    mortgage: int = 0
    administrative_fee: int = 0
    repair_fee: int = 0
    electricity: int = 0
    gas: int = 0
    water: int = 0
    electricity_usage_in_kwh: int = 0
    gas_usage_in_m3: int = 0
    water_usage_in_m3: int = 0
    internet: int = 0
    cable_tv: int = 0
    tennis_club: int = 0
    pilates: int = 0
    nhk: int = 0
    car_parking: int = 0
    bicycle_parking: int = 0
    car_management : int = 0
    creditcard_visa: int = 0
    creditcard_view: int = 0
    creditcard_mc: int = 0
    basic_life: int = 0


class IncomeByItemEntity(BaseModel):
    """ Entity which holds income info by income attribute """
    report_date: str
    updated_on: datetime
    item_key: str
    item_value: int = 0
    item_labels: list
