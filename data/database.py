from sqlalchemy.orm.session import Session


from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from utils.paths import resource_path

DATABASE_NAME = "app.db"

DATABASE_PATH = resource_path("data", DATABASE_NAME)
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"



engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}

)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()