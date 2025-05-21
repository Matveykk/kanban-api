from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.board.models import Column, Project


class BoardAccessTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner", password="strong-pass-1")
        self.other = User.objects.create_user("other", password="strong-pass-2")

    def _auth(self, user):
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": user.username, "password": "strong-pass-1" if user == self.owner else "strong-pass-2"},
        )
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_requires_authentication(self):
        response = self.client.get(reverse("project-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_project(self):
        self._auth(self.owner)
        response = self.client.post(reverse("project-list"), {"name": "Board"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.get().owner, self.owner)

    def test_user_sees_only_own_projects(self):
        Project.objects.create(name="Mine", owner=self.owner)
        Project.objects.create(name="Theirs", owner=self.other)
        self._auth(self.owner)
        response = self.client.get(reverse("project-list"))
        names = [p["name"] for p in response.data]
        self.assertEqual(names, ["Mine"])

    def test_cannot_access_foreign_project(self):
        foreign = Project.objects.create(name="Theirs", owner=self.other)
        self._auth(self.owner)
        response = self.client.get(reverse("project-detail", args=[foreign.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_flow(self):
        self._auth(self.owner)
        project = Project.objects.create(name="Board", owner=self.owner)
        column = Column.objects.create(project=project, name="Todo")
        response = self.client.post(
            reverse("task-list"),
            {"column": column.id, "title": "First task", "priority": 2},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RegistrationTests(APITestCase):
    def test_register_and_login(self):
        response = self.client.post(
            reverse("register"),
            {"username": "newuser", "email": "n@test.io", "password": "another-pass-9"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        login = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "newuser", "password": "another-pass-9"},
        )
        self.assertIn("access", login.data)
