""" Values """
from pydantic import BaseModel
from pydantic import Field

# pylint: disable=too-few-public-methods


class LabelValue(BaseModel):
    """ Labels for each key """
    report_date: list = Field([''], const=True)
    updated_on: list = Field([''], const=True)
    income_tax: list = Field(['withholding_tax'], const=True)
    resident_tax: list = Field(['other_tax_and_insurance'], const=True)
    life_insurance: list = Field(['other_tax_and_insurance'], const=True)
    employment_insurance: list = Field(['other_tax_and_insurance'], const=True)
    health_insurance: list = Field(['other_tax_and_insurance'], const=True)
    nursing_insurance: list = Field(['other_tax_and_insurance'], const=True)
    welfare_pension: list = Field(['other_tax_and_insurance'], const=True)
    savings: list = Field(['asset'], const=True)
    securities: list = Field(['asset'], const=True)
    n401k: list = Field(['asset'], const=True)
    mortgage: list = Field(['cashout', 'lifeline'], const=True)
    administrative_fee: list = Field(['cashout', 'lifeline'], const=True)
    repair_fee: list = Field(['cashout', 'lifeline'], const=True)
    electricity: list = Field(['cashout','lifeline'], const=True)
    gas: list = Field(['cashout','lifeline'], const=True)
    water: list = Field(['cashout','lifeline'], const=True)
    electricity_usage_in_kwh: list = Field(['lifeline'], const=True)
    gas_usage_in_m3: list = Field(['lifeline'], const=True)
    water_usage_in_m3: list = Field(['lifeline'], const=True)
    internet: list = Field(['cashout', 'service'], const=True)
    cable_tv: list = Field(['cashout', 'service'], const=True)
    tennis_club: list = Field(['cashout', 'service'], const=True)
    pilates: list = Field(['cashout', 'service'], const=True)
    nhk: list = Field(['cashout', 'service'], const=True)
    car_parking: list = Field(['cashout', 'service'], const=True)
    bicycle_parking: list = Field(['cashout', 'service'], const=True)
    car_management: list = Field(['cashout', 'service'], const=True)
    creditcard_visa: list = Field(['cashout','creditcard'], const=True)
    creditcard_view: list = Field(['cashout','creditcard'], const=True)
    creditcard_mc: list = Field(['cashout','creditcard'], const=True)
    basic_life: list = Field(['cashout'], const=True)
