import telebot
import os
from main import *
import keyboard
import threading
import time

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
            result = create_pdf_file(False)
            if result is False:
                bot.send_message(message.chat.id, "Новых заказов нет!", parse_mode="HTML",
                                 reply_markup=keyboard.MainKeyboard)
            else:
                text = "Готово!" if (not result[1]) else "Возьмите новый лист!"
                try:
                    bot.send_message(message.chat.id, text, parse_mode="HTML",
                                     reply_markup=keyboard.MainKeyboard)
                    bot.send_document(
                        message.chat.id, open('result.pdf', 'rb'))
                except:
                    print("Ошибка")


def posting():
    while True:
        delivers = get_awaiting_deliver()
        if delivers != []:
            for user in USERS:
                bot.send_message(
                    user, "Новый заказ!", parse_mode="HTML", reply_markup=keyboard.MainKeyboard)
        time.sleep(400)


th1 = threading.Thread(target=posting, )
th1.start()
th1.join()


bot.polling(none_stop=True, interval=0)
