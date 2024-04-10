
from sqlalchemy.orm import Session
from app.schemas import usersRegJson
from app.schemas import authUser
from app.Models import Users

def create_user(users:usersRegJson,db: Session):
    user = Users(
        email=users.email,
        password = users.password,
        name = users.name,
        surname = users.surname
    )
    db.add(user)
    db.commit()
    db.refresh(user)


def findUser(users:authUser,db: Session):
    query = db.query(Users).filter(Users.email == users.email,Users.password ==users.password).first()
    return query.id
def authenticate_user(users:authUser,db: Session):
    email = validate_email(users.email,db)
    password = validate_password(users.password,db)
    if email and password:
        return 2
    elif not email:
        return 1
    elif not password:
        return 0


def validate_email(email:str,db:Session):
    user = db.query(Users).filter(Users.email == email).first()
    if user is None:
        return False
    else:
        return True



def validate_password(password:str,db:Session):
    user = db.query(Users).filter(Users.password == password).first()
    if user is None:
        return False
    else:
        return True