import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import faker
import random


# Пароль от бд: 20130927
#                                                       пароль            название таблицы
engine = create_engine('postgresql+psycopg2://postgres:20130927@localhost/rebotica') # Устанавливаем  соединения с бд

Base = declarative_base() # Обязательная строка перед созданием классов таблиц

class Users(Base): # Создание класса таблицы, столбцы совпадают с pgadmin
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(250), nullable=False)
    hp = Column(Integer, default=100)
    dmg = Column(Integer, default=20)

Base.metadata.create_all(engine) # Обязательная строка после создания классов таблиц

Session = sessionmaker(bind=engine) # Создаем класс Сессии
s = Session() # Создаем объект класса Сессии

# hero = Users(id=123, name='Keks') # Создаем строку таблицы users в виде объекта класса Users
# s.add(hero) # Добавлям строку в таблицу
# s.commit() # Сохраняем изменения этой сессии

fake = faker.Faker('ru_RU')

# Добавили в таблицу 400 рандомных записей
# for x in range(400):
#     user_id = random.randint(1000, 9999)
#     name = fake.first_name()
#     obj = Users(id=user_id, name=name)
#     s.merge(obj)
#     s.commit()

# Запросили и вывели все записи
data = s.query(Users).all()
for user in data:
    print(user.name)
print()

# Запросили и вывели записи, где id больше 1500
data = s.query(Users).filter(Users.id > 1500)
for user in data:
    print(f'id: {user.id}, name: {user.name}')
print()

# Запросили и вывели записи, где id больше 1500 и меньше 1700
data = s.query(Users).filter(Users.id > 1500, Users.id < 1700)
for user in data:
    print(f'id: {user.id}, name: {user.name}')
print()

# Заменили имя в записи с id 1531
s.query(Users).filter(Users.id == 1531).update({"name": "Lee"})
s.commit()

# Удалили запись с id 1602
s.query(Users).filter(Users.id == 1602).delete()
s.commit()

data = s.query(Users).filter(Users.id > 1500, Users.id < 1700)
for user in data:
    print(f'id: {user.id}, name: {user.name}')

