from fastapi import FastAPI, Depends, HTTPException
from fastapi import APIRouter
from typing import Annotated

from starlette import status

from app.schemas import usersRegJson , authUser
from pydantic import BaseModel
from sqlalchemy.orm import Session
import app.crud as crud
from app.Models import Services
from app.database import SessionLocal
from app.schemas import EmployeesJson
from app.schemas import ZapisJson, ZapisJsonForCreate
from app.schemas import ServiceJson
import app.crudCalendar as crudCalendar
import app.crudServices as crudServices
import app.usersCrud as usersCrud
from app.schemas import Response
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
@router.get("/employee/getAll/{user_id}")
async def getAllEmployee(db:db_dependency,user_id:int):
    return crud.getAll(db,user_id)
@router.post("/employee/update/{id}")
async def updateEmployee(emp:EmployeesJson,db:db_dependency,id:int):
    return crud.update(emp,db,id)
@router.delete("/employee/delete/{id}")
async def deleteEmployee(id:int,db:db_dependency):
    return crud.delete(db,id)

@router.post("/calendar/create")
async def createCalendar(zapis:ZapisJsonForCreate,db:db_dependency):
    return crudCalendar.create(zapis,db)
@router.get("/calendar/getAll")
async def getAllCalendar(db:db_dependency):
    return crudCalendar.getAll(db)
@router.post("/calendar/update/{id}")
async def updateCalendar(zapis:ZapisJsonForCreate,db:db_dependency,id:int):
    return crudCalendar.update(id,db,zapis)
@router.delete("/calendar/delete/{id}")
async def deleteCalendar(id:int,db:db_dependency):
    return crudCalendar.delete(id,db)

@router.get("/services/getAll/{user_id}")
async def getAllServices(db:db_dependency):
    return crudServices.getAll(db)
@router.post("/services/update/{service_id}/")
async def updateServices(services:ServiceJson, db:db_dependency, service_id:int):
    return crudServices.updateService(services, db,service_id)
@router.delete("/services/delete/{service_id}")
async def deleteServices(db:db_dependency,service_id:int):
    return crudServices.deleteService(db,service_id)
@router.post("/services/create")
async def createServices(db:db_dependency, services:ServiceJson):
    return crudServices.createService(services,db)

@router.post("/users/create")
async def createUsers(user:usersRegJson,db:db_dependency):
    usersCrud.create_user(user,db)

@router.post("/users/auth")
async def auth(user:authUser,db:db_dependency):
    temp = usersCrud.authenticate_user(user,db)
    if temp == 2:
        return usersCrud.findUser(user,db)
    elif temp == 1:
        return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email is incorrect",

    )
    elif temp == 0:
        return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Password is incorrect",

    )