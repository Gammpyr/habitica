from django.db import models

from config import settings


# Create your models here.


class Habit(models.Model):
    """Модель полезной привычки"""
    #TODO: Реализовать: Нельзя выполнять привычку реже, чем 1 раз в 7 дней.

    PERIODICITY = (
        ('', 'не выбрано'),
        ('day', 'ежедневная'),
        ('week', 'еженедельная'),
        ('month', 'ежемесячная'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.DateTimeField(verbose_name='Время')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_good = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='related_habits',
        verbose_name='Связанная привычка'
    )
    periodicity = models.CharField(choices=PERIODICITY, default='day', max_length=255, verbose_name='Периодичность')
    reward = models.CharField(max_length=255, null=True, blank=True,verbose_name='Вознаграждение ')
    time_to_do = models.PositiveIntegerField(verbose_name='Время на выполнение (в секундах)')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']