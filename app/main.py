import asyncio
import json
import time
import random
from fastapi.responses import HTMLResponse
import sqlalchemy as sql
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.openapi.models import Response
from sqlalchemy import event

from sqlalchemy.future import select
from pydantic import BaseModel

from app.routes import router
import app.Models as Models
from typing import Annotated
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session
import datetime
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from app.schemas import WebSocketFinancesJson
app = FastAPI()
Models.Base.metadata.create_all(bind=engine)
finances = sql.Table('Finances', sql.MetaData(), autoload_with=engine)
app.include_router(router, prefix="", tags=[""])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['GET','POST','DELETE'],
    allow_headers=["*"],
)
class Finances(BaseModel):
    date: datetime.date
    operation_type: str
    sum: float
    sender: str
    comment: str



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/finances/create")
async def create_finances(Finances: Finances, db: db_dependency):
    db_Finances = Models.Finances(date=Finances.date, operation_type=Finances.operation_type, sum=Finances.sum,
                                  sender=Finances.sender,
                                  comment=Finances.comment,
                                  time = datetime.datetime.now().time().strftime('%H:%M'),
                                  user_id = Finances.user_id
                                  )
    db.add(db_Finances)
    db.commit()
    db.refresh(db_Finances)
    await after_data_insert(None, None, db_Finances)
    return  db.query(Models.Finances).filter(Models.Finances.date == Finances.date,
                                             Models.Finances.operation_type == Finances.operation_type,
                                             Models.Finances.sum == Finances.sum,
                                             Models.Finances.sender == Finances.sender,
                                             Models.Finances.comment == Finances.comment,
                                             Models.Finances.user_id == Finances.user_id
                                             ).first()


@app.get("/finances/{id}")
async def get(id: int, db: db_dependency):

    query = db.query(Models.Finances).filter(Models.Finances.id == id).first()
    print(datetime.datetime.now())
    return query


@app.get("/finances/getAll/{user_id}")
async def getAll(db: db_dependency,user_id:int):
    query = db.query(Models.Finances).filter(Models.Finances == user_id).all()
    return query
@app.post("/financeUpdate/{id}")
async def update(Finances: Finances ,db :db_dependency,id:int ):

    query = db.query(Models.Finances).filter(Models.Finances.id == id).first()
    query.date=Finances.date
    query.operation_type = Finances.operation_type
    query.sum = Finances.sum
    query.sender = Finances.sender
    query.comment = Finances.comment
    db.commit()
    db.refresh(query)

@app.delete("/financesDelete/{id}")
async def delete(db: db_dependency,id:int ):
    query = db.query(Models.Finances).filter(Models.Finances.id == id).first()
    db.delete(query)
    db.commit()




class ConnectionManager:
        def __init__(self):
            self.active_connections: list[WebSocket] = []

        async def connect(self, websocket: WebSocket):
            await websocket.accept()
            self.active_connections.append(websocket)

        def disconnect(self, websocket: WebSocket):
            self.active_connections.remove(websocket)


        async def broadcast(self,finances:WebSocketFinancesJson):
            for connection in self.active_connections:
                temp =DTOtoJson(finances)
                print(temp)

                await connection.send_json(temp)

manager = ConnectionManager()
@app.websocket("/finances/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket,db:db_dependency,user_id:int):
    await manager.connect(websocket)

    try:
        listOfFinances = db.query(Models.Finances).filter(Models.Finances.user_id == user_id).all()
        for finance in listOfFinances:
            temp = DTO(finance)
            await manager.broadcast(temp)
            await asyncio.sleep(1)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@event.listens_for(Models.Finances, "after_insert")
async def after_data_insert(mapper, connection, target):
    new_data = target
    print(DTOtoJson(DTO(new_data)))
    await asyncio.sleep(3)
    await manager.broadcast(DTO(new_data))
def DTO(finances:Models.Finances)->WebSocketFinancesJson:
    temp = WebSocketFinancesJson(
        date = finances.date,
        operation_type = finances.operation_type,
        sum = finances.sum,
        sender = finances.sender,
        comment =  finances.comment,
        time = finances.time
    )
    return temp
def DTOtoJson(finances:WebSocketFinancesJson):
    data = json.dumps(
        {
        "data": str(finances.date),
        "operation_type":finances.operation_type,
        "sum": finances.sum,
        "sender": finances.sender,
        "comment": finances.comment,
        "time": str(finances.time)
    }
    )

    return data