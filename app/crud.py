from app.models import *
from app.extensions import scoped_session
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user

def create_user(db: scoped_session, name: str, password: str):
    if not db.query(User).filter(User.name==name).first():
        user = User(name=name, hashed_password=generate_password_hash(password))
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        raise BadRequest("User already exists")

def read_user(db: scoped_session, name: str):
    user = db.query(User).filter(User.name==name).first()
    if user:
        return user
    else:
        return False

def update_user(db: scoped_session, name: str, new_name: str):
    user = db.query(User).filter(User.name==name).first()
    if user:
        user.name = new_name
    else:
        raise NotFound("User not found")    
    db.commit()
    db.refresh(user)

def delete_user(db: scoped_session, name: str):
    user = read_user(db, name)
    if user:
        db.delete(user)
        db.commit()
        db.refresh(user)
    else: 
        raise NotFound("User not found")

def check_password(user: User, password: str):
    return check_password_hash(user.hashed_password, password)


# def create_task(db: scoped_session, title: str, description: str, tags: list[str]):
#     task = Task(
#         title=title,
#         description=description,
#         task_date=date.today(),
#         owner=current_user,
#         owner_id=current_user.id,
#         )
#     for name in tags:
#         tag = db.query(Tag).filter(Tag.name==name).first()
#         if tag:
#             task.tags.append(tag)
#         else:
#             create_tag(db, name)
#             task.tags.append(tag)
#     db.add(task)
#     db.commit()
#     db.refresh(task)

def create_task(db: scoped_session, title: str, description: str, tags: list):
    task = Task(
            title=title,
            description=description,
            task_date=date.today(),
            owner=current_user,
            owner_id=current_user.id,
            tags=tags
        )
    db.add(task)
    db.commit()
    db.refresh(task)

def read_task(db: scoped_session, task_id: int):
    task = db.query(Task).filter(Task.id==task_id).first()
    if task:
        return task
    else:
        raise NotFound("Task not found")

def update_task(db: scoped_session, task_id: int, title: str, description: str, tags: list[str]):
    task = db.query(Task).filter(Task.id==task_id).first()
    if task:
        task.title = title
        task.description = description
        task.tags = []
        for name in tags:
            tag = db.query(Tag).filter(Tag.name==name).first()
            if tag:
                task.tags.append(tag)
            else:
                create_tag(db, name)
                task.tags.append(tag)
        db.commit()
        db.refresh(task)
    else:
        raise NotFound("Task not found")

def delete_task(db: scoped_session, task_id: int):
    task = db.query(Task).filter(Task.id==task_id).first()
    if task:
        db.delete(task)
        db.commit()
        db.refresh(task)
    else:
        raise NotFound("Task not found")


def create_tag(db: scoped_session, name: str):
    tag = db.query(Tag).filter(Tag.name==name).first()
    if not tag:
        db.add(tag)
        db.commit()
        db.refresh(tag)
    else:
        raise BadRequest("Tag already exists")

def delete_tag(db: scoped_session, name: str):
    tag = db.query(Tag).filter(Tag.name==name).first()
    if not tag:
        db.delete(tag)
        db.commit()
        db.refresh(tag)
    else:
        raise NotFound("Tag not found")
