from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import logging
import information

logging.basicConfig(format="%(levelname)-8s [%(asctime)s] %(message)s", level=logging.INFO, filename="bot.log")


def hello(bot, update):

    keyboard = [[InlineKeyboardButton("Сырный бургер", callback_data='1'),
                 InlineKeyboardButton("Бургер-Хуюргер", callback_data='2'),
                 InlineKeyboardButton("БляБудуЭтотБургер", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выберите хавчик:', reply_markup=reply_markup)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Не знаю такой команды")


def reply(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def button(bot, update):
    query = update.callback_query
    if query.data == '1':
        bot.edit_message_text(text="Цена: 123 рубля",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        bot.send_photo(chat_id=query.message.chat_id, photo='https://xn--80afnuz7f.xn--p1acf/a/gazmyas/files//import'
                                                            '/1bdd905d-8028-4a84-894e-e2192661a872_1522932012_iiko'
                                                            '.jpg')
    if query.data == '2':
        bot.edit_message_text(text="Цена: 224 рубля",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        bot.send_photo(chat_id=query.message.chat_id, photo='http://ugli-club.ru/wp-content/uploads/2017/11'
                                                            '/product_img_54.jpg')

    if query.data == '3':
        bot.edit_message_text(text="Цена: 333 рубля",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        bot.send_photo(chat_id=query.message.chat_id, photo='http://burgergroup.ru/content/uploads/2017/10/Dvoynoy'
                                                            '-Mesto-Burger-675x450.jpg')


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
