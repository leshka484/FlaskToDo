from datetime import date

from flask_login import current_user
from sqlalchemy import select
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import scoped_session
from app.models import Tag, Task, User


def create_user(db: scoped_session, name: str, password: str) -> None:
    if db.execute(select(User).where(User.name == name)).scalar_one_or_none():
        raise BadRequest("User already exists")
    user = User(name=name, hashed_password=generate_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)


def read_user(db: scoped_session, name: str) -> User:
    user = db.execute(select(User).where(User.name == name)).scalar_one_or_none()
    if user:
        return user
    raise NotFound("User not found")


def update_user(db: scoped_session, name: str, new_name: str) -> None:
    user = read_user(db=db, name=name)
    user.name = new_name
    db.commit()
    db.refresh(user)


def delete_user(db: scoped_session, name: str) -> None:
    user = read_user(db, name)
    db.delete(user)
    db.commit()


def check_password(user: User, password: str) -> bool:
    return check_password_hash(str(user.hashed_password), password)


def create_task(db: scoped_session, title: str, description: str, tags: list) -> None:
    task = Task(
        title=title,
        description=description,
        task_date=date.today(),
        owner=current_user,
        owner_id=current_user.id,
        tags=tags,
    )
    db.add(task)
    db.commit()
    db.refresh(task)


def read_task(db: scoped_session, task_id: int) -> Task:
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task:
        return task
    else:
        raise NotFound("Task not found")


def update_task(
    db: scoped_session, task_id: int, title: str, description: str, tags: list
) -> None:
    task = read_task(db=db, task_id=task_id)
    task.title = title
    task.description = description
    task.tags = tags
    db.commit()
    db.refresh(task)


def delete_task(db: scoped_session, task_id: int) -> None:
    task = read_task(db=db, task_id=task_id)
    db.delete(task)
    db.commit()


def create_tag(db: scoped_session, name: str) -> None:
    if db.execute(select(Tag).where(Tag.name == name)).scalar_one_or_none():
        raise BadRequest("User already exists")
    tag = Tag(name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)


def read_tag(db: scoped_session, name: str) -> Tag:
    tag = db.execute(select(Tag).where(Tag.name == name)).scalar_one_or_none()
    if tag:
        return tag
    raise NotFound("Tag not found")


def delete_tag(db: scoped_session, name: str) -> None:
    tag = read_tag(db=db, name=name)
    db.delete(tag)
    db.commit()
