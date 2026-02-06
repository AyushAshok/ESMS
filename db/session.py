from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URL_DATABASE='postgresql://postgres:ayush@localhost:5432/ESMS'

engine=create_engine(URL_DATABASE)

SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)