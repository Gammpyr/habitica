from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token["username"] = user.username
        token["email"] = user.email

        return token


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit"""

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'telegram_chat_id', 'date_joined']
        exclude = ['password', 'is_superuser', 'is_staff', 'user_permissions', 'groups']
