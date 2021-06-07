"""Data models for use with notifications"""

from enum import Enum
from typing import List

from pydantic import BaseModel, constr


class Carrier(BaseModel):
    name: str
    extension: str


class CarrierList(BaseModel):
    carriers: List[Carrier]


class Contact(BaseModel):
    name: str = "<unknown>"
    number: constr(regex=r"\d{3}-\d{3}-\d{4}")
    carrier: str
