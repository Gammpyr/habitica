from celery import shared_task
from django.utils import timezone

from habitica.models import Habit
from habitica.services import send_telegram_message


@shared_task
def send_telegram_notification(chat_id, message):
    """Задача для отправки уведомлений в Telegram"""
    print("Отправка в Telegram...")
    send_telegram_message(chat_id, message)

    print(f"Отправка в Telegram chat_id={chat_id}: {message}")
    return True


@shared_task
def check_and_send_habit_reminders():
    """Основная задача: проверка и отправка напоминаний"""
    now_local = timezone.localtime()
    now = now_local.time()

    habits = Habit.objects.filter(
        time__hour=now.hour, time__minute=now.minute
    ).select_related("user")

    for habit in habits:
        if habit.user.telegram_chat_id:
            message = f"""
Напоминание!

Пришло время выполнить привычку:
{habit.action}

Время: {habit.time.strftime('%H:%M')}
Место: {habit.place}
Время на выполнение: {habit.time_to_do} секунд!
"""
            periodicity = {
                "day": 1,
                "two_days": 2,
                "three_days": 3,
                "four_days": 4,
                "five_days": 5,
                "six_days": 6,
                "week": 7,
            }

            required_interval = periodicity.get(habit.periodicity)
            if required_interval:
                days_since_last = (now_local.date() - habit.last_notified.date()).days

                if days_since_last < required_interval:
                    continue

            send_telegram_notification.delay(
                chat_id=habit.user.telegram_chat_id, message=message
            )
            habit.last_notified = timezone.now()
            habit.save()
            print(f"Напоминание отправлено для привычки: {habit.action}")
        else:
            print(f"У пользователя {habit.user.username} нет telegram_chat_id ")
