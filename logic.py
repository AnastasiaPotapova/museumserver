import logging
from telegram import Update, Poll
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, PollAnswerHandler, CallbackContext
from collections import defaultdict
from datetime import timedelta
import asyncio

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Хранилище для голосов
votes = defaultdict(dict)

# ID топика, куда отправлять результаты (замените на нужный)
TOPIC_ID = 123456789  # Замените на ваш ID топика


# Функция для создания опроса
async def start_poll(update: Update, context: CallbackContext) -> None:
    question = "Какое ваше любимое время года?"
    options = ["Зима", "Весна", "Лето", "Осень"]

    poll_message = await context.bot.send_poll(
        chat_id=update.message.chat_id,
        question=question,
        options=options,
        is_anonymous=False,  # Чтобы видеть, кто за что голосовал
        allows_multiple_answers=False,
        message_thread_id=TOPIC_ID  # Отправка опроса в определённый топик
    )

    # Сохраняем данные о созданном опросе
    context.job_queue.run_once(send_poll_results, when=timedelta(days=1), context={
        'poll_message_id': poll_message.poll.id,
        'chat_id': update.message.chat_id,
        'message_thread_id': TOPIC_ID  # Указание ID топика для итогового сообщения
    })


# Функция для сохранения голосов
async def receive_poll_answer(update: Update, context: CallbackContext) -> None:
    answer = update.poll_answer
    poll_id = answer.poll_id
    user_id = answer.user.id
    option_ids = answer.option_ids

    # Сохраняем голос
    votes[poll_id][user_id] = option_ids


# Функция для отправки результатов опроса через день
async def send_poll_results(context: CallbackContext) -> None:
    poll_message_id = context.job.context['poll_message_id']
    chat_id = context.job.context['chat_id']
    message_thread_id = context.job.context['message_thread_id']

    poll = context.bot_data.get(poll_message_id)
    results = votes.get(poll_message_id, {})

    results_message = "Итоги опроса:\n\n"

    for user_id, options in results.items():
        user = await context.bot.get_chat(user_id)
        selected_options = ', '.join([poll.options[option_id].text for option_id in options])
        results_message += f"{user.first_name} выбрал(а): {selected_options}\n"

    await context.bot.send_message(
        chat_id=chat_id,
        text=results_message,
        parse_mode=ParseMode.HTML,
        message_thread_id=message_thread_id  # Отправка итогов в указанный топик
    )


# Основная функция
async def main() -> None:
    # Создание приложения
    application = Application.builder().token("7148422286:AAGlA84bt50tlz2sOfciv4xfRka5hR5rJB4").build()

    # Добавление обработчиков
    application.add_handler(CommandHandler('startpoll', start_poll))
    application.add_handler(PollAnswerHandler(receive_poll_answer))

    # Запуск бота
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Удерживаем приложение в работе
    try:
        await application.updater.idle()
    except KeyboardInterrupt:
        print("Bot stopped.")


if __name__ == '__main__':
    asyncio.run(main())
