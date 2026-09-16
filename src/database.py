from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path

database_path = Path(__file__).parent.parent / 'data' / 'meeting_agent.db'
DATABASE_URL = f"sqlite:///{str(database_path)}"

engine = create_engine(
    url=DATABASE_URL,
    connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False   
)

Base = declarative_base()