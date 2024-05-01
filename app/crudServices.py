from app.Models import Services
from app.schemas import ServiceJson
from sqlalchemy.orm import Session

def getById(db: Session, id: int):
    return db.query(Services).filter(Services.id == id).first()
def getAll(db: Session,user_id:int):
    return db.query(Services).filter(Services.user_id == user_id).all()

def createService(json:ServiceJson,db: Session):
    service = Services(name = json.name,
                       sum = json.sum,
                       operation_type = json.operation_type,
                       time = json.time,
                       user_id = json.user_id)
    db.add(service)
    db.commit()
    db.refresh(service)
    return db.query(Services).filter(Services.name == json.name,
                                     Services.sum == json.sum,
                                     Services.operation_type == json.operation_type,
                                     Services.time == json.time,
                                     Services.user_id == json.user_id
                                     ).first()

def updateService(json:ServiceJson,db: Session,id: int):
    service = getById(db,id)
    service.name = json.name
    service.sum = json.sum
    service.operation_type = json.operation_type
    service.time = json.time
    db.commit()
    db.refresh(service)

def deleteService(db: Session,id: int):
    service = getById(db,id)
    db.delete(service)
    db.commit()