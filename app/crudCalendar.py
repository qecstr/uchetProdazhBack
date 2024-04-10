from sqlalchemy.orm import Session
from app.schemas import ZapisJson, CalendarJsonFinished
from app.Models import Calendar



def getByid(id:int,db:Session):
    return db.query(Calendar).filter(Calendar.id == id).first()
def create(zapis:ZapisJson,db:Session):
    db_emp = Calendar(

        operation_type = zapis.operation_type,
        name = zapis.name,
        sum = zapis.sum,
        date = zapis.date,
        comments = zapis.comments,
        time = zapis.time)
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db.query(Calendar).filter(
        Calendar.operation_type == zapis.operation_type,
        Calendar.name == zapis.name,
        Calendar.sum == zapis.sum,
        Calendar.date == zapis.date,
        Calendar.comments == zapis.comments,
        Calendar.time == zapis.time).first()

def getAll(db:Session):
    result = []
    for emp in db.query(Calendar).all():
        a = db.query(Calendar).filter(Calendar.date == emp.date).all()
        zapises = []
        for item in a:
            kk = ZapisJson(
                id = item.id,
                operation_type = item.operation_type,
                name = item.name,
                sum = item.sum,
                date = item.date,
                comments = item.comments,
                time = item.time
            )
            zapises.append(kk)
        temp = CalendarJsonFinished(
            date = emp.date,
            Zapis = zapises
        )
        result.append(temp)

    sortedResult = []
    for item in result:
        if item not in sortedResult:
            sortedResult.append(item)
    return sortedResult

def update(id:int,db:Session,zapis:ZapisJson):
    temp = getByid(id, db)
    temp.operation_type = zapis.operation_type,
    temp.name = zapis.name,
    temp.sum = zapis.sum,
    temp.date = zapis.date,
    temp.comments = zapis.comments,
    temp.time = zapis.time

    db.commit()
    db.refresh(temp)

def delete(id:int,db:Session):
    temp = getByid(id, db)
    db.delete(temp)
    db.commit()
