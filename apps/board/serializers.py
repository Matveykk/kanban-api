from rest_framework import serializers

from apps.board.models import Column, Project, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id", "column", "title", "description", "priority",
            "position", "assignee", "created_at", "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def validate_column(self, column):
        request = self.context["request"]
        if column.project.owner_id != request.user.id:
            raise serializers.ValidationError("column does not belong to your project")
        return column


class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Column
        fields = ("id", "project", "name", "position", "tasks")

    def validate_project(self, project):
        request = self.context["request"]
        if project.owner_id != request.user.id:
            raise serializers.ValidationError("project does not belong to you")
        return project


class ProjectSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ("id", "name", "description", "owner", "created_at", "columns")
        read_only_fields = ("owner", "created_at")
