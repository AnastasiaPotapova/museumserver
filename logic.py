import telebot
from telebot import types
from threading import Thread, Timer
from datetime import datetime, timedelta
import time
import json
from db import db, VisitModel, PollModel
from calend import update_event_from_calendar

botTimeWeb = telebot.TeleBot('7148422286:AAGlA84bt50tlz2sOfciv4xfRka5hR5rJB4')

a = types.InputPollOption('yes')
b = types.InputPollOption('no')
options = [a, b]
dt = 0
chat_id = -1002183010951
remind_thread_id = 2
poll_thread_id = 2
visits_thread_id = 2


def set_options():
    with open("replayScript.json", "r") as jsonFile:
        data = json.load(jsonFile)
    data["location"] = "NewPath"
    with open("replayScript.json", "w") as jsonFile:
        json.dump(data, jsonFile)


@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    chat_id = message.chat.id


@botTimeWeb.message_handler(commands=['set_poll'])
def set_poll(message):
    poll_thread_id = message.thread.id


@botTimeWeb.message_handler(commands=['set_remind'])
def set_remind(message):
    remind_thread_id = message.thread.id


@botTimeWeb.message_handler(commands=['set_visits'])
def set_visits(message):
    visits_thread_id = message.thread.id


votes = []
@botTimeWeb.poll_answer_handler()
def handle_poll_answer(poll_answer):
    nm = VisitModel(db.get_connection())
    user_id = poll_answer.user.id
    user_name = poll_answer.user.username
    option_ids = poll_answer.option_ids
    data = nm.get_all()
    for i in option_ids:
        vote = nm.get_vote(poll_answer.poll_id, i)
        nm.set_user(user_id, user_name, vote[0])
    data = nm.get_all()


def make_tg_poll(poll_ans):
    poll = botTimeWeb.send_poll(chat_id, 'Экскурсии недели', [x[1] for x in poll_ans], False, allows_multiple_answers=True,
                         message_thread_id=poll_thread_id)
    nm = PollModel(db.get_connection())
    nm.insert(poll.id)
    nm = VisitModel(db.get_connection())
    for i in range(len(poll_ans)):
        nm.insert(poll.poll.id, poll_ans[i][0], i)


def print_all_votes():
    for us in votes:
        mention = "[@" + us[1] + "](tg://user?id=" + str(us[0]) + ")"
        response = f"Hi, {mention}, "
        botTimeWeb.send_message(chat_id, text=response, parse_mode="Markdown", message_thread_id=2)


def make_remind_data(current_date):
    dt = current_date + " 20:00"
    remind_date = datetime.strptime(dt, "%Y-%m-%d %H:%M") - timedelta(days=1)
    pass


def print_remind(target_date, target_time):
    while True:
        current_time = datetime.now().strftime("%H:%M")
        current_date = str(datetime.now().date())
        if current_time == target_time and current_date == target_date:
            print_all_votes()
        time.sleep(60)


def check_poll_ans():
    pass


#Thread(target=botTimeWeb.infinity_polling).start()
#reminder_time = "18:00"
#check_ans_time = "23:59"
#make_tg_poll([[0, '1'],[1, '2'],[2, '3']])
#target_date = "2024-10-03"
#target_time = "13:52"
#Thread(target=reminder, args=(target_date, target_time)).start()