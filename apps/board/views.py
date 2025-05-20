from rest_framework import viewsets

from apps.board.models import Column, Project, Task
from apps.board.permissions import IsProjectOwner
from apps.board.serializers import ColumnSerializer, ProjectSerializer, TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectOwner]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ColumnViewSet(viewsets.ModelViewSet):
    serializer_class = ColumnSerializer
    permission_classes = [IsProjectOwner]

    def get_queryset(self):
        return Column.objects.filter(project__owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsProjectOwner]

    def get_queryset(self):
        return Task.objects.filter(column__project__owner=self.request.user)
