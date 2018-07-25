from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import logging
import information

from parser import Parser

logging.basicConfig(format="%(levelname)-8s [%(asctime)s] %(message)s", level=logging.INFO, filename="bot.log")

# TEMP SOLUTION FOR DEMO:
with open('cloudResponse.json', 'r') as f:
    s = f.read()
menu = parser(s)
categories = menu.getCategoriesList()

def hello(bot, update):
    reply_markup = getKeyboard(categories)
    update.message.reply_text('Что же будет на этот раз? :', reply_markup=reply_markup)

def dishMenu(category):
    dishes_list = menu.getDishesList(category) 
    callback_data = [category + '.' + x for x in dishes_list]
    reply_markup = getKeyboard(dishes_list, callback_data)
    update.message.reply_text('Как понять, что ты выбрал свое блюдо?' 
            'Очень легко: они все твои ;-)',
            reply_markup=reply_markup)

def getDishDescription(title):
    description = menu.getDishPage(title)
    pic = description.split('\n')[-1].split(': ')[-1]
    description = description.split('\n')[:-1]
    bot.edit_message_text(text=description,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    bot.send_photo(chat_id=query.message.chat_id, photo=pic)

def getKeyboard(l, callback_data=l):
    keyboard = [[]]
    for i in range(len(l)):
        keyboard[0].append(InlineKeyboardButton(l[i], callback_data=callback_data[i]))
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Не знаю такой команды")


def reply(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def button(bot, update):
    query = update.callback_query
    if query.data in categories:
        dishMenu(query.data)
    if '.' in query.data: # category.dish_title need to make more pretty
        getDishDescription(query.data)


def start_bot():
    updater = Updater(token=information.token, request_kwargs={
        'proxy_url': 'socks5://t1.learn.python.ru:1080',
        'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}
    })

    dp = updater.dispatcher

    hello_handler = CommandHandler('menu', hello)
    dp.add_handler(hello_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)

    reply_handler = CommandHandler('rep', reply)
    dp.add_handler(reply_handler)

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    start_bot()
