# Kanban Board API

REST API для канбан-доски задач на Django REST Framework с аутентификацией по JWT.

## Возможности

- Иерархия «проект → колонка → задача» с полным CRUD
- Аутентификация по JWT (access/refresh токены)
- Разграничение доступа: пользователь видит и меняет только свои проекты
- Приоритеты и позиции задач, назначение исполнителя
- Документация OpenAPI/Swagger по адресу `/api/docs/`

## Стек

Python, Django REST Framework, PostgreSQL, JWT (SimpleJWT), Docker.

## Структура

```
config/        настройки, URL-роутинг, WSGI
apps/accounts/ регистрация и выдача JWT-токенов
apps/board/    модели, сериализаторы, вьюсеты и права доступа
```

## Запуск

```bash
cp .env.example .env
docker compose up --build
```

Swagger UI: `http://localhost:8000/api/docs/`

## Аутентификация

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "email": "u@test.io", "password": "strong-pass-1"}'

curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "strong-pass-1"}'
```

Полученный `access`-токен передаётся в заголовке: `Authorization: Bearer <token>`.

## Основные эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/auth/register/` | Регистрация |
| POST | `/api/auth/token/` | Получение JWT |
| CRUD | `/api/projects/` | Проекты |
| CRUD | `/api/columns/` | Колонки |
| CRUD | `/api/tasks/` | Задачи |

## Тесты

```bash
python manage.py test
```
