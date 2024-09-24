from flask import Flask, render_template, redirect, request, jsonify
from add_news import AddEventForm, AddPeopleForm, EditPeopleForm
from db import PeopleModel, EventModel, DB
from calend import send_to_calendar, update_event_from_calendar
from logic import send_poll_ex
import json

app = Flask(__name__)

app.config.update(dict(
    DEBUG=False,
    MAIL_SERVER='smtp.yandex.ru',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='nast-pota@ya.ru',
    MAIL_PASSWORD='gjnfgjdf10',
))

db = DB()


@app.route('/')
@app.route('/events')
def events():
    events = EventModel(db.get_connection()).get_all()
    return render_template('chain.html', type=1,
                           data=events)


@app.route('/delete_event/<int:event_id>', methods=['GET'])
def delete_event(event_id):
    nm = EventModel(db.get_connection())
    nm.delete(str(event_id))
    return redirect("/events")


@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        etype = request.form["event_type"]
        date = request.form["event_date"]
        time = request.form["event_time"]
        user = request.form["event_user"]
        grade = request.form["event_grade"]
        pupil_number = request.form["event_pupil_number"]
        get_list = request.form["event_get_list"]
        get_payment = request.form["event_get_payment"]
        comment = request.form["event_comment"]
        nm = EventModel(db.get_connection())
        nm.insert(etype, date, time, user, grade, pupil_number, get_list, get_payment, comment)
        send_to_calendar(etype, date, time, user, grade, pupil_number, get_list, get_payment, comment)
        return redirect("/events")
    return render_template('add_event.html', title='Добавление Экскурсии', data="Vova")


@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    nm = EventModel(db.get_connection())
    event = nm.get(event_id)
    if request.method == 'POST':
        user = request.form["event_user"]
        grade = request.form["event_grade"]
        pupil_number = request.form["event_pupil_number"]
        get_list = request.form["event_get_list"]
        get_payment = request.form["event_get_payment"]
        comment = request.form["event_comment"]
        nm = EventModel(db.get_connection())
        nm.edit(event_id, user, grade, pupil_number, get_list, get_payment, comment)
        return redirect("/events")
    return render_template('edit_event.html', title='Редактирование Экскурсии',
                           data=event)


@app.route('/people')
def people():
    people = PeopleModel(db.get_connection()).get_all()
    return render_template('chain.html', type=2,
                           data=people)


@app.route('/delete_people/<int:people_id>', methods=['GET'])
def delete_people(people_id):
    nm = PeopleModel(db.get_connection())
    nm.delete(people_id)
    return redirect("/people")


@app.route('/delete_duty/<int:people_id>', methods=['GET'])
def delete_duty(people_id):
    nm = PeopleModel(db.get_connection())
    nm.set_duty(people_id)
    return redirect("/people")


@app.route('/add_people', methods=['GET', 'POST'])
def add_people():
    form = AddPeopleForm()
    if form.validate_on_submit():
        rfid = form.peoplerfid.data
        name = form.peoplename.data
        nm = PeopleModel(db.get_connection())
        nm.insert(rfid, name)
        return redirect("/people")
    return render_template('add_people.html', title='Добавление Экскурсовода',
                           form=form)


@app.route('/update_event', methods=['GET'])
def update_event():
    events = update_event_from_calendar()
    nm = EventModel(db.get_connection())
    for event in events:
        flag = nm.exist(event[1], event[2], event[0])
        if not flag:
            nm.insert(event[0], event[1], event[2])
    return redirect("/events")


@app.route('/edit_people/<int:people_id>', methods=['GET', 'POST'])
def edit_people(people_id):
    form = EditPeopleForm()
    nm = PeopleModel(db.get_connection())
    people = nm.get(people_id)
    if form.validate_on_submit():
        name = form.peoplename.data
        nm = PeopleModel(db.get_connection())
        nm.edit(people_id, name)
        return redirect("/people")
    return render_template('edit_people.html', title='Редактирование Экскурсии',
                           form=form)


@app.route('/check', methods=['POST'])
def check():
    rfid = request.data
    nm = PeopleModel(db.get_connection())
    people = nm.getrfid(str(rfid))
    if people:
        nm.use_event(people[0])
    else:
        nm.insert(str(rfid))
    return jsonify({'task': 'good'}), 201


app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

if __name__ == '__main__':
    app.run(port=5738, host='0.0.0.0')
