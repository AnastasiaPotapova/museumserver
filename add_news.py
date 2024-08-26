from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class AddEventForm(FlaskForm):
    event_type = StringField('Тип Экскурсии', validators=[DataRequired()])
    event_data = StringField('Дата Экскурсии', validators=[DataRequired()])
    event_time = StringField('Время Экскурсии', validators=[DataRequired()])
    event_user = StringField('Кто записал', validators=[DataRequired()])
    event_grade = StringField('Номер класса', validators=[DataRequired()])
    event_pupil_number = StringField('Количество детей', validators=[DataRequired()])
    event_get_list = StringField('Есть ли список', validators=[DataRequired()])
    event_get_payment = StringField('Прошла ли оплата', validators= [DataRequired()])
    event_comment = TextAreaField('Комментарий')
    submit = SubmitField('Добавить')


class AddPeopleForm(FlaskForm):
    peoplename = StringField('Имя', validators=[DataRequired()])
    peoplerfid = TextAreaField('rfid', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class EditPeopleForm(FlaskForm):
    peoplename = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('Изменить')
