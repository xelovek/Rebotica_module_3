import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


# Пароль от бд: 20130927
engine = create_engine('postgresql+psycopg2://root:20130927>@localhost/rebotica')

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(250), nullable=False)
    hp = Column(Integer, default=100)
    damage = Column(Integer, default=20)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
s = Session()

hero = Users(id=123, name='Keks')
s.add(hero)
s.commit()

