from fastapi import FastAPI, Depends
from fastapi import APIRouter
from typing import Annotated

from pydantic import BaseModel
from sqlalchemy.orm import Session
import app.crud as crud
from app.database import SessionLocal
from app.schemas import EmployeesJson
from app.schemas import ZapisJson
import app.crudCalendar as crudCalendar


router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/employee/get/{id}")
async def getByID(id:int,db:db_dependency):
    return crud.getByid(id,db)

@router.post("/employee/create")
async def create(emp:EmployeesJson,db:db_dependency):
    return crud.create(emp,db)
@router.get("/employee/getAll")
async def getAll(db:db_dependency):
    return crud.getAll(db)
@router.post("/employee/update/{id}")
async def update(emp:EmployeesJson,db:db_dependency,id:int):
    return crud.update(emp,db,id)
@router.delete("/employee/delete/{id}")
async def delete(id:int,db:db_dependency):
    return crud.delete(db,id)

@router.post("/calendar/create")
async def createCalendar(zapis:ZapisJson,db:db_dependency):
    return crudCalendar.create(zapis,db)
@router.get("/calendar/getAll")
async def getAllCalendar(db:db_dependency):
    return crudCalendar.getAll(db)
@router.post("/calendar/update")
async def update(zapis:ZapisJson,db:db_dependency,id:int):
    return crudCalendar.update(id,db,zapis)
@router.delete("/calendar/delete")
async def delete(id:int,db:db_dependency):
    return crudCalendar.delete(id,db)