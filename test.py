from parser import Parser

with open('cloudResponse.json', 'r') as f:
    data = f.read()

p = Parser(data)
# print(p.getDishesList('Бургеры'))
# print('=' * 80)
# print(p.getDishesList('Шаурма'))
# print('=' * 80)
# print(p.getDishPage('Бургеры.Бургер под номером!0'))
# print('=' * 80)
# print(p.getCategoriesList())

#
# ef button(bot, update):
#     query = update.callback_query
#     if query.data in categories:
#         dishes_list = menu.getDishesList(query.data)
#         callback_data = [query.data + '.' + x for x in dishes_list]
#         reply_markup = getKeyboard(dishes_list, callback_data)
#         bot.edit_message_text(text="Цена: 123 рубля",
#                               chat_id=query.message.chat_id,
#                               message_id=query.message.message_id)        # dishMenu(bot, update, query.data)
#     if '.' in query.data:  # category.dish_title need to make more pretty
#         getDishDescription(bot, update, query.data)