import requests

from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_URL


def send_telegram_message(chat_id, message):
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    response = requests.get(
        f"{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage", params=params
    )
    return response


#
# def check_if_need_send_reminder(habit, current_hour, current_minute):
#     """Проверка, пришло ли время отправлять напоминание для привычки"""
#     habit_hour = habit.time.hour
#     habit_minute = habit.time.minute
#
#     return habit_hour == current_hour and habit_minute == current_minute
