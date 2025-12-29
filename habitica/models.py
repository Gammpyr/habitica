from django.db import models

from config import settings

# Create your models here.


class Habit(models.Model):
    """Модель полезной привычки"""

    PERIODICITY = (
        ("", "не выбрано"),
        ("day", "ежедневная"),
        ("two_days", "каждые два дня"),
        ("three_days", "каждые три дня"),
        ("four_days", "каждые четыре дня"),
        ("five_days", "каждые пять дней"),
        ("six_days", "каждые шесть дней"),
        ("week", "еженедельная"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_good = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_habits",
        verbose_name="Связанная привычка",
    )
    periodicity = models.CharField(choices=PERIODICITY, default="day", max_length=255, verbose_name="Периодичность")
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name="Вознаграждение ")
    time_to_do = models.PositiveIntegerField(verbose_name="Время на выполнение (в секундах)")
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    last_notified = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Последнее уведомление"
    )
    last_completed = models.DateTimeField(null=True, blank=True, verbose_name="Последнее выполнение")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]

    def __str__(self):
        if self.is_good:
            return f"Приятная привычка: {self.action} в {self.time.strftime('%H:%M')}"
        else:
            return f"Полезная привычка: {self.action} в {self.time.strftime('%H:%M')}"
