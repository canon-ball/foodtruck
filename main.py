from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import PreCheckoutQueryHandler, ShippingQueryHandler
from telegram import LabeledPrice, ShippingOption

import logging
import information

from parser import Parser

logging.basicConfig(format="%(levelname)-8s [%(asctime)s] %(message)s", level=logging.INFO, filename="bot.log")

# TEMP SOLUTION FOR DEMO:
with open('cloudResponse.json', 'r') as f:
    s = f.read()
menu = Parser(s)
categories = menu.getCategoriesList()


def hello(bot, update):
    reply_markup = getKeyboard(categories)
    update.message.reply_text('Что же будет на этот раз? :', reply_markup=reply_markup)


def dishMenu(bot, update, category):
    dishes_list = menu.getDishesList(category)
    callback_data = [category + '.' + x for x in dishes_list]
    reply_markup = getKeyboard(dishes_list, callback_data)
    bot.send_message(chat_id=update.callback_query.message.chat_id, text='Как понять, что ты выбрал свое блюдо? '
                                                                         'Очень легко: они все твои ;-)',
                     reply_markup=reply_markup)

    # bot.edit_message_text(text='Как понять, что ты выбрал свое блюдо?'
    #                            'Очень легко: они все твои ;-)',
    #                       chat_id=update.callback_query.message.chat_id,
    #                       reply_markup=reply_markup)
    # update.message.reply_text('Как понять, что ты выбрал свое блюдо?'
    #                           'Очень легко: они все твои ;-)',
    #                           reply_markup=reply_markup)


def getDishDescription(bot, update, title):
    description = menu.getDishPage(title)
    pic = description.split('\n')[-1].split(': ')[-1]
    description = description.split('\n')[:-1]
    bot.send_message(chat_id=update.callback_query.message.chat_id, text="Охуительный состав: Мясо хлеб и ноль приправ")
    bot.send_photo(chat_id=update.callback_query.message.chat_id, photo='https://images.aif.ru/008/828'
                                                                        '/655ed6060ce02d0bde852f0ce32feaea.jpg')
    keyboard = [[InlineKeyboardButton("Оплатить", callback_data='4242')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update.callback_query.message.chat_id, text="Цена: 399 рублей", reply_markup=reply_markup)


def getKeyboard(l, callback_data=None):
    if not callback_data:
        callback_data = l
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
    if query.data == '4242':
        start_without_shipping_callback(bot, update)
    if query.data in categories:
        dishMenu(bot, update, query.data)
    if '.' in query.data:  # category.dish_title need to make more pretty
        getDishDescription(bot, update, query.data)


# PAYMENT


def start_without_shipping_callback(bot, update):
    chat_id = update.callback_query.message.chat_id
    title = "Payment Example"
    description = "Payment Example using python-telegram-bot"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    provider_token = "381764678:TEST:6257"
    start_parameter = "test-payment"
    currency = "RUB"
    # price in RUB
    price = 7000
    prices = [LabeledPrice("Test", price)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    bot.sendInvoice(chat_id, title, description, payload,
                    provider_token, start_parameter, currency, prices)


def precheckout_callback(bot, update):
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Custom-Payload':
        # answer False pre_checkout_query
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=False,
                                      error_message="Something went wrong...")
    else:
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)


# finally, after contacting to the payment provider...
def successful_payment_callback(bot, update):
    # do something after successful receive of payment?
    update.message.reply_text("Спасибо за покупку и приятного аппетита!")


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

    # Add command handler to start the payment invoice
    dp.add_handler(CommandHandler("pay", start_without_shipping_callback))

    # Pre-checkout handler to final check
    dp.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    dp.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    start_bot()
