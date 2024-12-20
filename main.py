from flask import Flask, render_template, redirect, request, jsonify
from add_news import AddEventForm, AddPeopleForm, EditPeopleForm
from db import PeopleModel, EventModel, db, VisitModel
from calend import send_to_calendar, update_event_from_calendar
from logic import make_tg_poll
import datetime
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


@app.route('/')
@app.route('/events')
def events():
    events = EventModel(db.get_connection()).get_all()
    data = []
    now = datetime.datetime.now()
    for event in events:
        current_date = event[2] + " 20:00"
        event_date = datetime.datetime.strptime(current_date, "%Y-%m-%d %H:%M")
        if event_date > now:
            data.append(event)
    return render_template('chain.html', type=1,
                           data=data)


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
    return render_template('add_event.html', title='Добавление Экскурсии')


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


@app.route('/people/<int:people_id>')
def people_page(people_id):
    people = PeopleModel(db.get_connection()).get(people_id)
    visits = VisitModel(db.get_connection()).get_by_user_id(people_id)
    print(visits)
    return render_template('people.html',
                           people=people, visits=visits)


@app.route('/add_visit/<int:people_id>')
def add_visit(people_id):
    now = datetime.datetime.now()
    date = str(now.date())
    visits = VisitModel(db.get_connection()).insert(date[-2:]+"."+date[5:7], str(now.ctime())[11:16], people_id)
    PeopleModel(db.get_connection()).add_event(people_id)
    return redirect(f"/people/{people_id}")


@app.route('/delete_visit/<int:visit_id>', methods=['GET'])
def delete_visit(visit_id):
    people_id = VisitModel(db.get_connection()).get(visit_id)[3]
    visit = VisitModel(db.get_connection()).delete(visit_id)
    PeopleModel(db.get_connection()).dell_event(people_id)
    return redirect(f"/people/{people_id}")


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


@app.route('/edit_people/<int:user_id>', methods=['GET', 'POST'])
def edit_people(user_id):
    nm = PeopleModel(db.get_connection())
    user = nm.get(user_id)
    if request.method == 'POST':
        user_name = request.form["user_name"]
        number_events = request.form["number_events"]
        duty = request.form["duty"]
        nm = PeopleModel(db.get_connection())
        nm.edit(user_id, user_name, number_events, duty)
        return redirect("/events")
    return render_template('edit_people.html', title='Редактирование Экскурсовода',
                           data=user)


@app.route('/check', methods=['POST'])
def check():
    rfid = str(request.data)[2:-1]
    nm = PeopleModel(db.get_connection())
    visit = VisitModel(db.get_connection())
    people = nm.getrfid(rfid)
    if people:
        nm.add_event(people[0])
        now = datetime.datetime.now()
        date = str(now.date())
        visit.insert(date[-2:]+"."+date[5:7], str(now.ctime())[11:16], people[0])
    else:
        nm.insert(rfid)
    return jsonify({'task': 'good'}), 201


@app.route('/make_poll', methods=['GET', 'POST'])
def make_poll():
    exmod = EventModel(db.get_connection())
    excursions = exmod.get_all()
    poll_ans = []
    if request.method == 'POST':
        for i in list(request.form):
            dt = exmod.get(i)
            poll_ans.append([dt[0], ' '.join([str(dt[1]), str(dt[2])[-5:], str(dt[3])[:5]])])
        make_tg_poll(poll_ans)
        return redirect("/events")
    return render_template('make_poll.html', data=excursions)


app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def update_rfid():
    pm = PeopleModel(db.get_connection())
    dt = pm.get_all()
    for p in dt:
        pm.set_rfid(p[0], p[2][6:-1].lower())

def run_server():
    app.run(port=5738, host='0.0.0.0')

update_rfid()
run_server()