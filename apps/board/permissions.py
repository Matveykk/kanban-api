from rest_framework import permissions

from apps.board.models import Column, Project, Task


class IsProjectOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return _project_of(obj).owner_id == request.user.id


def _project_of(obj):
    if isinstance(obj, Project):
        return obj
    if isinstance(obj, Column):
        return obj.project
    if isinstance(obj, Task):
        return obj.column.project
    raise TypeError("unsupported object type")
