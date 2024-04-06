from app.Models import Services
from app.schemas import ServiceJson
from sqlalchemy.orm import Session

def getById(db: Session, id: int):
    return db.query(Services).filter(Services.id == id).first()
def getAll(db: Session):
    return db.query(Services).all()

def createService(json:ServiceJson,db: Session):
    service = Services(name = json.name,sum = json.sum,operation_type = json.operation_type,time = json.time)
    db.add(service)
    db.commit()
    db.refresh(service)

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