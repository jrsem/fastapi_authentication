# para criar/abrir uma session num banco de dados
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base 
from sqlalchemy import create_engine
import os

load_dotenv()


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
db=create_engine(SQLALCHEMY_DATABASE_URL)

# criar a base do banco de dados
Base=declarative_base()

def get_session():
    # criar/abrir uma session no nosso banco de dados
    try:
        Session=sessionmaker(bind=db)
        session=Session()
        yield session
    finally:
        session.close()