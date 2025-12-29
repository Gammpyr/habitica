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
Заполните .env файл 

3. Установите зависимости
```bash
    poetry install
```
4. Настройка базы данных
```
# Создание и активация виртуального окружения
poetry shell

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser
```

5. Запуск сервера
```bash
    poetry run python manage.py runserver
```

## Развертывание на сервере

1. Подготовка сервера
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv postgresql redis-server nginx docker.io
```
2. База данных PostgreSQL

```bash
sudo -u postgres psql
# В консоли PostgreSQL:
CREATE DATABASE habitica;
CREATE USER habitica WITH PASSWORD 'habitica';
GRANT ALL PRIVILEGES ON DATABASE habitica TO habitica;
\q
```

3. Настройка Redis

```bash
sudo systemctl start redis
sudo systemctl enable redis
```
4. Развертывание приложения
```bash
git clone <repository-url> /opt/habitica
cd /opt/habitica
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
5. Gunicorn сервис
Создайте /etc/systemd/system/habitica.service:
```ini
[Unit]
Description=Habitica Django Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/habitica
Environment="PATH=/opt/habitica/venv/bin"
ExecStart=/opt/habitica/venv/bin/gunicorn --workers 3 --bind unix:/opt/habitica/habitica.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
```
```bash
bash
sudo systemctl start habitica
sudo systemctl enable habitica
```
6. Настройка Nginx
Создайте /etc/nginx/sites-available/habitica:

```nginx
server {
    listen 80;
    server_name 158.160.215.227;

    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/habitica/habitica.sock;
    }
}
```
```bash
sudo ln -s /etc/nginx/sites-available/habitica /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

7. Celery сервисы
Создайте /etc/systemd/system/celery.service:

```ini
[Unit]
Description=Celery Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/habitica
Environment="PATH=/opt/habitica/venv/bin"
ExecStart=/opt/habitica/venv/bin/celery -A config worker -l INFO

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl start celery
sudo systemctl enable celery
```

## CI/CD настройка
1. GitHub Actions
 - Создайте .github/workflows/ci.yml
2. Docker Compose для продакшн
 - Создайте docker-compose.prod.yml
3. GitHub Secrets
Добавьте в настройках репозитория:

 - DOCKER_USERNAME

 - DOCKER_TOKEN

 - SERVER_HOST 

 - SERVER_USER 

 - SSH_PRIVATE_KEY
  
## API Endpoints
### Аутентификация
POST /users/api/token/ - Получение JWT токена

POST /users/api/token/refresh/ - Обновление токена

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