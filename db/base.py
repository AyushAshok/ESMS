from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL_DATABASE='postgresql://postgres:ayush@localhost:5432/ESMS'

# engine=create_engine(URL_DATABASE)

# SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base=declarative_base()