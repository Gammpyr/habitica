from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    telegram_chat_id = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="ID чата в Telegram"
    )

    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ['username']
    fields = ['id', 'username', 'email', 'telegram_chat_id', 'date_joined']
    exclude = ['password', 'is_superuser', 'is_staff', 'user_permissions', 'groups']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} - {self.email}"
