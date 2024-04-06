from fastapi import FastAPI, Depends
from fastapi import APIRouter
from typing import Annotated

from pydantic import BaseModel
from sqlalchemy.orm import Session
import app.crud as crud
from app.Models import Services
from app.database import SessionLocal
from app.schemas import EmployeesJson
from app.schemas import ZapisJson
from app.schemas import ServiceJson
import app.crudCalendar as crudCalendar
import app.crudServices as crudServices

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/employee/get/{id}")
async def getByIDEmployee(id:int,db:db_dependency):
    return crud.getByid(id,db)

@router.post("/employee/create")
async def createEmployee(emp:EmployeesJson,db:db_dependency):
    return crud.create(emp,db)
@router.get("/employee/getAll")
async def getAllEmployee(db:db_dependency):
    return crud.getAll(db)
@router.post("/employee/update/{id}")
async def updateEmployee(emp:EmployeesJson,db:db_dependency,id:int):
    return crud.update(emp,db,id)
@router.delete("/employee/delete/{id}")
async def deleteEmployee(id:int,db:db_dependency):
    return crud.delete(db,id)

@router.post("/calendar/create")
async def createCalendar(zapis:ZapisJson,db:db_dependency):
    return crudCalendar.create(zapis,db)
@router.get("/calendar/getAll")
async def getAllCalendar(db:db_dependency):
    return crudCalendar.getAll(db)
@router.post("/calendar/update/{id}")
async def updateCalendar(zapis:ZapisJson,db:db_dependency,id:int):
    return crudCalendar.update(id,db,zapis)
@router.delete("/calendar/delete/{id}")
async def deleteCalendar(id:int,db:db_dependency):
    return crudCalendar.delete(id,db)

@router.get("/services/getAll")
async def getAllServices(db:db_dependency):
    return crudServices.getAll(db)
@router.post("/services/update/{id}")
async def updateServices(services:ServiceJson, db:db_dependency, service_id:int):
    return crudServices.updateService(services, db,service_id)
@router.delete("/services/delete/{id}")
async def deleteServices(db:db_dependency,service_id:int):
    return crudServices.deleteService(db,service_id)
@router.post("/services/create")
async def createServices(db:db_dependency, services:ServiceJson):
    return crudServices.createService(services,db)