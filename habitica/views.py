from django.db.models import Q
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
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
            if self.action in ["update", "partial_update", "destroy", "complete"]:
                return Habit.objects.filter(user=user)
            return Habit.objects.filter(Q(user=user) | Q(is_public=True))

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

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        habit = self.get_object()
        if habit.user != request.user:
            return Response({"error": "Вы не можете выполнять чужую привычку"}, status=status.HTTP_403_FORBIDDEN)
        habit.last_completed = timezone.now()
        habit.save()
        return Response({"status": "habit completed"})
