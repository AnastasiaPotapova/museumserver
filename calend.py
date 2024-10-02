from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

# 1. Настроить учетные данные (скачайте JSON-файл учетных данных из Google Cloud Console)
SERVICE_ACCOUNT_FILE = 'museum-vk-bot-ce02c57d683b.json'
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
    time_max = one_week_ago.isoformat() + 'Z'  # 'Z' обозначает UTC-время
    time_min = now.isoformat() + 'Z'
    print(time_min, time_max)
    # 4. Получаем события за последнюю неделю
    events_result = service.events().list(calendarId='7b1561e0938ce1f98aa164640148e7b8f541c95dec8a9dedf8de9a3045426463@group.calendar.google.com', timeMin=time_min, timeMax=time_max,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    # 5. Обработка и вывод событий
    if not events:
        return None
    else:
        return events


def update_event_from_calendar():
    data = get_from_calendar()
    ans = []
    for event in data:
        start = event['start'].get('dateTime', event['start'].get('date'))
        ans.append([event['summary'].split()[0], start[0:10], start[11:-4]])
    return ans