import telebot
from telebot import types
from threading import Thread, Timer
from datetime import datetime
import time
from calend import update_event_from_calendar

botTimeWeb = telebot.TeleBot('7148422286:AAGlA84bt50tlz2sOfciv4xfRka5hR5rJB4')

a = types.InputPollOption('yes')
b = types.InputPollOption('no')
options = [a, b]
dt = 0


@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    print(message.chat.id)


votes = {}
@botTimeWeb.poll_answer_handler()
def handle_poll_answer(poll_answer):
    user_id = poll_answer.user.id
    user_name = poll_answer.user.username
    option_ids = poll_answer.option_ids
    selected_options = [options[i].text for i in option_ids]
    votes[user_id] = [selected_options, user_name]


def make_tg_poll(poll_ans):
    poll = botTimeWeb.send_poll(-1002183010951, 'Экскурсии недели', poll_ans, False, allows_multiple_answers=True,
                         message_thread_id=2)


def print_all_votes():
    for user, options in votes.items():
        mention = "[@" + options[1] + "](tg://user?id=" + str(user) + ")"
        response = f"Hi, {mention}, {options[0]}"

        botTimeWeb.send_message(chat_id=-1002183010951, text=response, parse_mode="Markdown", message_thread_id=2)


def reminder(target_date, target_time):
    while True:
        current_time = datetime.now().strftime("%H:%M")
        current_date = str(datetime.now().date())
        if current_time == target_time and current_date == target_date:
            print_all_votes()
        time.sleep(60)


def check_poll_ans():
    pass


Thread(target=botTimeWeb.infinity_polling).start()
reminder_time = "18:00"
check_ans_time = "23:59"
make_tg_poll(['1', '2', '3'])
target_date = "2024-10-03"
target_time = "13:52"
Thread(target=reminder, args=(target_date, target_time)).start()