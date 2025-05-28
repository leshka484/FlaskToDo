from datetime import date
from typing import List

from flask_login import UserMixin
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import Base


class User(Base, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, default="Без названия")
    description: Mapped[str] = mapped_column(String, index=True)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    task_date: Mapped[date] = mapped_column(Date, default=date.today)
    owner: Mapped[User] = relationship("User", back_populates="tasks")
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary="tasks_tags", back_populates="tasks"
    )


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    tasks: Mapped[List["Task"]] = relationship(
        "Task", secondary="tasks_tags", back_populates="tags"
    )


tasks_tags = Table(
    "tasks_tags",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)
