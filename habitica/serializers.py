from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit"""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, data):
        related_habit = data.get("related_habit")

        reward = data.get("reward")
        if related_habit and reward:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать и связанную привычку и вознаграждение"
            )

        time_to_do = data.get("time_to_do")
        if time_to_do and time_to_do > 120:
            raise serializers.ValidationError(
                "Время выполнения должно быть не больше 120 секунд."
            )

        if related_habit and not related_habit.is_good:
            raise serializers.ValidationError("Связанная привычка должна быть приятной")

        is_good = data.get("is_good", self.instance.is_good if self.instance else False)
        if is_good and reward:
            raise serializers.ValidationError(
                "Приятная привычка не может иметь вознаграждение"
            )
        if is_good and related_habit:
            raise serializers.ValidationError(
                "Приятная привычка не может иметь связанную привычку"
            )

        periodicity = data.get(
            "periodicity", self.instance.periodicity if self.instance else "day"
        )
        if not is_good and periodicity == "month":
            raise serializers.ValidationError(
                {
                    "periodicity": "Полезная привычка не может выполняться реже, чем 1 раз в 7 дней."
                }
            )

        return data
