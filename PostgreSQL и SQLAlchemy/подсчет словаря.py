from db import *


# Если функция len() считает кол-во элементов в списке\кортеже\словаре или строке
# Что нужно положить в скобки функции len()?

users = s.query(Users).all()
print(users)
result = {}
for user in users:
    result[user.name] = len(s.query(Users).filter(Users.name == user.name).all())
print(result)
for key in result:
    print(key, ':', result[key])

