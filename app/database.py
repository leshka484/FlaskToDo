import os
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from dotenv import load_dotenv

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

engine = create_engine(os.environ.get("DATABASE_URL"))
SessionLocal = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = SessionLocal.query_property()

def init_db():
    import app.models
    Base.metadata.create_all(bind=engine)

# session = SessionLocal()
# print(session.execute(text('SELECT 1')).scalar())  # Должно вывести: 1
