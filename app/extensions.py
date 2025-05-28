import os
from pathlib import Path

from dotenv import load_dotenv
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

login_manager = LoginManager()  # Настройки для Flask-login

load_dotenv(dotenv_path=Path(__file__).parent / ".env")  # Настройки SQLAlchemy

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

engine = create_engine(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
)
Session = scoped_session(sessionmaker(bind=engine))


class Base(DeclarativeBase):
    pass
