# Habitica - Трекер привычек

API для трекера полезных привычек с интеграцией Telegram для отправки уведомлений.

### Основные возможности
 - Создание, редактирование и удаление привычек

 - Публичные и приватные привычки

 - Напоминания о привычках через Telegram


### Технологии
 - Python 3.13

 - Django 5.2

 - Django REST Framework

 - PostgreSQL

 - Redis

 - Celery

 - JWT аутентификация

### Установка
1. Клонирование репозитория
```bash
    git clone <repository-url>
    cd Habitica
```
2. Настройка окружения
```bash
    cp .env.example .env
```
 - Заполните .env файл

3. Установите зависимости
```bash
    poetry install
```
4. Запуск сервера
```bash
    poetry run python manage.py runserver
```

## API Endpoints
### Аутентификация
POST /users/token/ - Получение JWT токена

POST /users/token/refresh/ - Обновление токена

### Привычки
GET /habits/ - Список привычек

POST /habits/ - Создание привычки

GET /habits/{id}/ - Получение привычки

PUT /habits/{id}/ - Обновление привычки

DELETE /habits/{id}/ - Удаление привычки

POST /habits/{id}/complete/ - Отметить выполнение

## Бизнес-правила
- Время выполнения привычки не более 120 секунд

- Нельзя одновременно указывать связанную привычку и вознаграждение

- Связанная привычка должна быть приятной

- Приятная привычка не может иметь вознаграждение

- Полезная привычка не может выполняться реже, чем 1 раз в 7 дней

- Каждый пользователь видит только свои привычки

- Публичные привычки видны всем пользователям

## Запуск worker и beat
```bash
    # Redis
    redis-server
```
```bash
    # Celery worker
    celery -A config worker -l INFO --pool=solo
```
```bash
    # Celery beat
    celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
## Тестирование
```bash
    # Запуск тестов
    python manage.py test
```
```bash
# С покрытием
coverage run manage.py test
coverage report
```

## Документация
Swagger UI: http://localhost:8000/swagger/

ReDoc: http://localhost:8000/redoc/