import os
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from dotenv import load_dotenv
from flask_login import LoginManager

login_manager = LoginManager()  # Настройки для Flask-login

load_dotenv(dotenv_path=Path(__file__).parent / ".env") # Настройки SQLAlchemy 
engine = create_engine(os.environ.get("DATABASE_URL"))
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = Session.query_property()
