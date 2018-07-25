from parser import Parser
with open('cloudResponse.json', 'r') as f:
	data = f.read()

p = Parser(data)
print(p.getDishesList('Бургеры'))
print('='*80)
print(p.getDishesList('Шаурма'))
print('='*80)
print(p.getDishPage('Бургеры.Бургер под номером!0'))
print('='*80)
print(p.getCategoriesList())
