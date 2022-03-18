from datetime import datetime
from pydantic import BaseModel

class IncomeByDateEntity(BaseModel):
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
    rent: int = 0
    electricity: int = 0
    gas: int = 0
    water: int = 0
    newspaper: int = 0
    cable_tv: int = 0
    tennis_club: int = 0
    pilates: int = 0
    nhk: int = 0
    parking: int = 0
    car: int = 0
    creditcard_visa: int = 0
    creditcard_view: int = 0
    creditcard_mc: int = 0
    basic_life: int = 0
    remote_work: int = 0

class IncomeByItemEntity(BaseModel):
    report_date: str
    updated_on: datetime
    item_key: str
    item_value: int = 0
    item_labels: list
