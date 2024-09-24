import telebot
from telebot import types
from threading import Thread, Timer
from datetime import datetime
import time

botTimeWeb = telebot.TeleBot('7148422286:AAGlA84bt50tlz2sOfciv4xfRka5hR5rJB4')


@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    a = types.InputPollOption('yes')
    b = types.InputPollOption('no')
    botTimeWeb.send_poll(message.chat.id, 'What would you choose?', [a, b], False, allows_multiple_answers=True, message_thread_id=2)
    print(message.chat.id)


@botTimeWeb.message_handler(func=lambda message: True)
def echo_message(message):
    botTimeWeb.reply_to(message, message.text)


def send_poll_ex():
    a = types.InputPollOption('yes')
    b = types.InputPollOption('no')
    botTimeWeb.send_poll(-1002183010951, 'What would you choose?', [a, b], False, allows_multiple_answers=True,
                         message_thread_id=2)


Thread(target=botTimeWeb.infinity_polling).start()


def run_once_at_time(target_date, target_time):
    while True:
        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().date()
        if current_time == target_time and current_date == target_date:
            send_poll_ex()
            break
        time.sleep(30)


# Установите время в формате 'ЧЧ:ММ'
target_time = "20:17"  # Например, 15:30
target_date = "2024-08-29"
Thread(target=run_once_at_time, args=(target_time, target_date)).start()