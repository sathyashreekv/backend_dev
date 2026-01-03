from sqlalchemy import create_engine ,Column,Integer,String,DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime , timezone

DATABASE_URL="sqlite:///./api_requests.db"
engine=create_engine(DATABASE_URL,connect_args={"check_same_thread":False})

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()
class APIRequest(Base):
    __tablename__='api_requests'
    id=Column(Integer, primary_key=True,index=True)
    endpoint=Column(String,index=True)
    method=Column(String)
    timmestamp=Column(DateTime,default=datetime.now(timezone.utc))
    response_time=Column(Float)
    status_code=Column(Integer)
Base.metadata.create_all(bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()




