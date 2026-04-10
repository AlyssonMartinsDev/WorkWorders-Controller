# sqlAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# variaveis de ambiente
import os
from dotenv import load_dotenv
load_dotenv() #carrega as variaveis de ambiente

# Variaveis
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# criando a endine
engine = create_engine(
    DATABASE_URL,
    echo=False
)

#criando a sessao
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#criando o base
Base = declarative_base()