
from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel
from app.Models import Calendar
import datetime
T = TypeVar('T')
class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]

class EmployeesJson(BaseModel):
    name: str
    surname: str
    speciality: str

class ServiceJson(BaseModel):
    name: str
    sum: float


class ZapisJson(BaseModel):
    operation_type: str
    name: str
    sum: float
    date: datetime.date
    comments: str
    time: datetime.time

class CalendarJsonFinished(BaseModel):
    date: datetime.date
    Zapis: List[ZapisJson]


