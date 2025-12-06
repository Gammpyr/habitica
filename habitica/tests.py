from datetime import time

from django.test import TestCase
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from habitica.models import Habit
from habitica.serializers import HabitSerializer
from users.models import CustomUser

# Create your tests here.


class HabitAPITestCase(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="test1", email="test1@test.ru", password="test1"
        )

        self.habit1 = Habit.objects.create(
            user=self.user1,
            place="test_place1",
            time=time(1, 0),
            time_to_do=60,
            action="test_action1",
        )

        self.habit2 = Habit.objects.create(
            user=self.user1,
            place="test_place2",
            time=time(2, 0),
            time_to_do=120,
            action="test_action2",
        )

    def test_get_habit_list(self):
        """
        Проверка получения списка привычек
        """
        self.client.force_authenticate(user=self.user1)

        response = self.client.get("/habits/")

        self.assertEqual(response.status_code, HTTP_200_OK)

        results = response.json()["results"]
        habit1 = results[0]
        habit2 = results[1]

        self.assertEqual(habit1["place"], "test_place1")
        self.assertEqual(habit1["time"], "01:00:00")
        self.assertEqual(habit1["time_to_do"], 60)
        self.assertEqual(habit1["action"], "test_action1")

        self.assertEqual(habit2["place"], "test_place2")
        self.assertEqual(habit2["time"], "02:00:00")
        self.assertEqual(habit2["time_to_do"], 120)
        self.assertEqual(habit2["action"], "test_action2")

    def test_str_method(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.habit1), "Полезная привычка: test_action1 в 01:00")

        # Проверяем для приятной привычки
        pleasant_habit = Habit.objects.create(
            user=self.user1,
            place="Кровать",
            time=time(3, 0),
            time_to_do=30,
            action="test_action3",
            periodicity="day",
            is_good=True,
        )

        self.assertEqual(str(pleasant_habit), "Приятная привычка: test_action3 в 03:00")

    def tearDown(self):
        Habit.objects.all().delete()
        CustomUser.objects.all().delete()


class HabitSerializerTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", password="test")

    def test_good_data(self):
        """True - должны проходить"""
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "action": "Пить воду",
            "time_to_do": 60,
            "is_good": False,
            "periodicity": "day",
        }

        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_bad_time_to_do(self):
        """Fasle: время > 120 секунд"""
        data = {
            "place": "Дом",
            "time": "09:00:00",
            "action": "Тест",
            "time_to_do": 150,
            "is_good": False,
            "periodicity": "day",
        }

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_bad_monthly_periodicity(self):
        """False: полезная привычка ежемесячная"""
        data = {
            "place": "Дом",
            "time": "10:00:00",
            "action": "Тест",
            "time_to_do": 60,
            "is_good": False,
            "periodicity": "month",  # Ошибка!
        }

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_good_and_reward(self):
        """False: приятная привычка с вознаграждением"""
        data = {
            "place": "Дом",
            "time": "11:00:00",
            "action": "Приятная",
            "time_to_do": 30,
            "is_good": True,
            "reward": "Шоколад",  # Ошибка!
        }

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
