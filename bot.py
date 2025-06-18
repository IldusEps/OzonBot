import telebot
import os
from main import *
import keyboard

# Инициализация телеграмм-бота
bot = telebot.TeleBot(os.getenv("TELEGRAM_API"))

USERS = [885172912, 1957670122]


@bot.message_handler(commands=['start'])
def start_message(message):
    """ Ввод команды /start в боте """
    bot.send_message(message.chat.id, "Привет", parse_mode="HTML",
                     reply_markup=keyboard.MainKeyboard)
    print(message.chat.id)


@bot.message_handler(content_types=['text'])
def text(message):
    if message.chat.id not in USERS:
        bot.send_message(message.chat.id, "Доступ к боту заблокирован", parse_mode="HTML",
                         reply_markup=keyboard.MainKeyboard)
        return False
    match message.text:
        case "Продолжить лист" | "Новый лист":
            if message.text == "Новый лист":
                dataBase.data_clear()
            bot.send_message(message.chat.id, "Ждите...", parse_mode="HTML",
                             reply_markup=keyboard.MainKeyboard)
            if create_pdf_file() == False:
                bot.send_message(message.chat.id, "Новых заказов нет!", parse_mode="HTML",
                                 reply_markup=keyboard.MainKeyboard)
            else:
                try:
                    bot.send_document(
                        message.chat.id, open('result.pdf', 'rb'))
                except:
                    print("Ошибка")


bot.polling(none_stop=True, interval=0)
