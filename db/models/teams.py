from sqlalchemy import Integer, String, Column
from ESMS.db.base import Base

class Teams(Base):
    __tablename__='teams'

    id=Column(Integer,primary_key=True,index=True,unique=True)
    name=Column(String,index=True,unique=True)