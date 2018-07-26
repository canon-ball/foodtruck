from json2message import Json2Message 

with open('cloudResponse.json', 'r') as f:
    data = f.read()

p = Json2Message(data)
print(p.getDishesList('Бургеры'))
print('=' * 80)
print(p.getDishesList('Шаурма'))
print('=' * 80)
print(p.getDishPage('Шаурма.Крученый рулет под номером 0'))
print('=' * 80)
print(p.getCategoriesList())

