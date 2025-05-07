from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, Boolean
from sqlalchemy.orm import relationship
from app.extensions import Base
from datetime import date

from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, default="Без названия")
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_date = Column(Date, default=date.today)  
    owner = relationship("User", back_populates="tasks")
    tags = relationship("Tag", secondary="tasks_tags", back_populates="tasks")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    tasks = relationship(
        "Task", secondary="tasks_tags", back_populates="tags"
    )
    
tasks_tags = Table(
    "tasks_tags",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)
