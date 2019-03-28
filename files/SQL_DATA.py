from sqlalchemy import String,Column,Integer,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine=create_engine("mysql+mysqlconnector://root:19918858@localhost:3306/crawl_data")
Base=declarative_base(bind=engine)
Session=sessionmaker(bind=engine)

class Crawl_data(Base):
    __tablename__='crawl_datas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_time = Column(String(32), nullable=False)
    co2 = Column(String(32), nullable=False)
    air_temp = Column(String(32), nullable=False)
    air_humidity = Column(String(32), nullable=False)
    illuminate = Column(String(32), nullable=False)
    soil_temp = Column(String(32), nullable=False)
    soil_humidity = Column(String(32), nullable=False)

def init():
    Base.metadata.create_all(engine)