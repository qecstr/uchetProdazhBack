
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
    user_id:int
class ServiceJson(BaseModel):
    name: str
    sum: float
    operation_type: str
    time: int
    user_id: int
class ZapisJson(BaseModel):
    id: int
    operation_type: str
    name: str
    sum: float
    date: datetime.date
    comments: str
    time: datetime.time
    user_id: int
class ZapisJsonForCreate(BaseModel):
    operation_type: str
    name: str
    sum: float
    date: datetime.date
    comments: str
    time: datetime.time
    user_id: int
class CalendarJsonFinished(BaseModel):
    date: datetime.date
    Zapis: List[ZapisJson]

class WebSocketFinancesJson(BaseModel):
    date: datetime.date
    operation_type: str
    sum: float
    sender: str
    comment: str
    time: datetime.time


class usersRegJson(BaseModel):
    email: str
    password: str
    name: str
    surname: str


class authUser(BaseModel):
    email:str
    password:str
class userView(BaseModel):
    id:int
    name:str
    surname:str
