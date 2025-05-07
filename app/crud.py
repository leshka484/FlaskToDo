from app.models import *
from app.extensions import scoped_session
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(db: scoped_session, name: str, password: str):
    if not db.query(User).filter(User.name==name).first():
        user = User(name=name, password=generate_password_hash(password))
        db.add(user)
        db.commit()
        db.refresh(user)
    raise BadRequest("User already exists")

def read_user(db: scoped_session, name: str):
    user = db.query(User).filter(User.name==name).first()
    if user:
        return user
    else:
        raise NotFound("User not found")  

def update_user(db: scoped_session, user: User):
    db.commit()
    db.refresh(user)

def delete_user(db: scoped_session, user: User):
    db.delete(user)
    db.commit()
    db.refresh(user)

def check_password(user: User, password: str):
    return check_password_hash(user.hashed_password, password)