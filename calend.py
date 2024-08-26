from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

# 1. Настроить учетные данные (скачайте JSON-файл учетных данных из Google Cloud Console)
SERVICE_ACCOUNT_FILE = 'museum-vk-bot-c31fb937a060.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# 2. Создаем объект для взаимодействия с Google Calendar API
service = build('calendar', 'v3', credentials=credentials)


def send_to_calendar(type, date, time, user, grade, number, list, payment, comment):
    datetime_value = date + ' ' + time
    dt = datetime.strptime(datetime_value, '%Y-%m-%d %H:%M')

    # Устанавливаем временную зону +03:00
    tz = timezone(timedelta(hours=3))
    dt = dt.replace(tzinfo=tz)

    # Преобразуем в строку формата ISO 8601
    iso_datetime_start = dt.isoformat()
    dt_end = dt + timedelta(hours=1)
    iso_datetime_end = dt_end.isoformat()
    event = {
        'summary': type + " Школьники",
        'description': "Ответственный:{}\nКласс:{}\nКолличество детей:{}\nОплата:{}".format(user, grade, number, payment),
        'start': {
            'dateTime': iso_datetime_start,
            'timeZone': 'Europe/Moscow',
        },
        'end': {
            'dateTime': iso_datetime_end,
            'timeZone': 'Europe/Moscow',
        }
    }

    # 4. Создаем событие в календаре
    event_result = service.events().insert(calendarId='tassiiyya@gmail.com', body=event).execute()


def get_from_calendar():
    # 3. Задаем временной диапазон - последняя неделя
    now = datetime.now()
    one_week_ago = now + timedelta(days=7)
    time_min = one_week_ago.isoformat() + 'Z'  # 'Z' обозначает UTC-время
    time_max = now.isoformat() + 'Z'

    # 4. Получаем события за последнюю неделю
    events_result = service.events().list(calendarId='tassiiyya@gmail.com', timeMin=time_min, timeMax=time_max,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    # 5. Обработка и вывод событий
    if not events:
        print('Нет событий за последнюю неделю.')
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"Событие: {event['summary']} Начало: {start}")

