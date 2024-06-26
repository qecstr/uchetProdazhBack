
from sqlalchemy.orm import Session
from app.schemas import EmployeesJson as Json
from app.Models import Employees




def getByid(id:int,db:Session):
    return db.query(Employees).filter(Employees.id == id).first()
def create(Employe:Json,db:Session):
    db_emp = Employees(name=Employe.name,surname= Employe.surname,speciality = Employe.speciality,user_id = Employe.user_id)
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db.query(Employees).filter(
                                        Employees.name == Employe.name,
                                        Employees.surname == Employe.surname,
                                        Employees.speciality == Employe.speciality,
                                        Employees.user_id == Employe.user_id
                                                    ).first()
def getAll(db:Session,user_id:int):
    return db.query(Employees).filter(Employees.user_id == user_id).all()

def update( emp:Json,db :Session,id:int):
    temp = getByid(id,db)
    temp.name = emp.name
    temp.surname = emp.surname
    temp.speciality = emp.speciality

    db.commit()
    db.refresh(temp)
def delete(db :Session,id:int):
    query = getByid(id,db)
    db.delete(query)
    db.commit()




