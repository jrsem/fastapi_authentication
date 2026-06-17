## CREER VIRTUAL ENVIRONMENT:
python3 -m venv venv

## ACTIVER VIRTUAL ENVIRONMENT:
source venv/bin/activate

## INSTALLER LES DEPENDANCES:
pip install -r requirements.txt

## EXECUTER:
fastapi dev main.py

## to create tables
# Initialize alembic
alembic init alembic

# Then run migrations
alembic upgrade head

## ==============================================
python3 -c "
import sys, os
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from app.db.models import User, Base
from app.db.dependencies import db
Base.metadata.create_all(bind=db)
print('Tables:', list(Base.metadata.tables.keys()))
"