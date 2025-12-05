from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from habitica.models import Habit
from habitica.pagination import HabitPagination
from habitica.permissions import IsOwner
from habitica.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            owner_habits = Habit.objects.filter(user=user)

            public_habits = Habit.objects.filter(is_public=True).exclude(user=user)

            return owner_habits.union(public_habits)

        else:
            return Habit.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
