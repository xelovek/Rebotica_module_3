import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:20130927@localhost/rebotica")
Base = declarative_base()


class Player(Base):
    __tablename__ = "gamers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    address = Column(String)
    x = Column(Integer, default=500)
    y = Column(Integer, default=500)
    size = Column(Integer, default=50)
    errors = Column(Integer, default=0)
    abs_speed = Column(Integer, default=2)
    speed_x = Column(Integer, default=2)
    speed_y = Column(Integer, default=2)
    def __init__(self, name, address):
        self.name = name
        self.address = address

Session = sessionmaker(bind=engine)
s = Session()
Base.metadata.create_all(engine) # Обязательная строка после создания классов таблиц