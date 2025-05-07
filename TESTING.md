# Инструкция по тестированию UniDoc

## Подготовка к тестированию

1. Запустите сервер разработки:
```bash
python manage.py runserver
```

2. Откройте браузер и перейдите по адресу:
- Swagger UI: http://127.0.0.1:8000/
- ReDoc: http://127.0.0.1:8000/redoc/
- Admin: http://127.0.0.1:8000/admin/

## Lesson 1: Основы Django

### Тестирование моделей

1. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

2. Войдите в админ-панель (http://127.0.0.1:8000/admin/):
- Проверьте создание темы
- Проверьте создание проекта
- Проверьте создание задачи
- Проверьте создание подзадачи
- Проверьте создание комментария
- Проверьте создание документа
- Проверьте создание шаблона

### Тестирование связей

1. В админ-панели:
- Создайте тему
- Создайте проект, связанный с темой
- Создайте задачу в проекте
- Создайте подзадачу в задаче
- Создайте комментарий к задаче
- Создайте документ в проекте
- Создайте шаблон для темы

## Lesson 2: Django REST Framework

### Тестирование API

1. Получите JWT токен:
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"your-password"}'
```

2. Сохраните полученный токен для использования в следующих запросах.

### Тестирование эндпоинтов

1. Темы:
```bash
# Получение списка тем
curl http://127.0.0.1:8000/api/topics/ \
     -H "Authorization: Bearer your-token"

# Создание темы
curl -X POST http://127.0.0.1:8000/api/topics/ \
     -H "Authorization: Bearer your-token" \
     -H "Content-Type: application/json" \
     -d '{"name":"Test Topic","description":"Test Description"}'

# Получение активных тем
curl http://127.0.0.1:8000/api/topics/active/ \
     -H "Authorization: Bearer your-token"
```

2. Проекты:
```bash
# Получение списка проектов
curl http://127.0.0.1:8000/api/projects/ \
     -H "Authorization: Bearer your-token"

# Создание проекта
curl -X POST http://127.0.0.1:8000/api/projects/ \
     -H "Authorization: Bearer your-token" \
     -H "Content-Type: application/json" \
     -d '{"name":"Test Project","topic":1}'

# Получение проектов с задачами
curl http://127.0.0.1:8000/api/projects/with-tasks/ \
     -H "Authorization: Bearer your-token"
```

3. Задачи:
```bash
# Получение списка задач
curl http://127.0.0.1:8000/api/tasks/ \
     -H "Authorization: Bearer your-token"

# Создание задачи
curl -X POST http://127.0.0.1:8000/api/tasks/ \
     -H "Authorization: Bearer your-token" \
     -H "Content-Type: application/json" \
     -d '{"title":"Test Task","project":1,"status":"new"}'

# Получение просроченных задач
curl http://127.0.0.1:8000/api/tasks/overdue/ \
     -H "Authorization: Bearer your-token"
```

## Lesson 3: Аутентификация и авторизация

### Тестирование JWT

1. Получение токена:
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"your-password"}'
```

2. Обновление токена:
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh":"your-refresh-token"}'
```

3. Проверка токена:
```bash
curl -X POST http://127.0.0.1:8000/api/token/verify/ \
     -H "Content-Type: application/json" \
     -d '{"token":"your-access-token"}'
```

### Тестирование прав доступа

1. Попытка доступа без токена:
```bash
curl http://127.0.0.1:8000/api/topics/
```

2. Попытка доступа с неверным токеном:
```bash
curl http://127.0.0.1:8000/api/topics/ \
     -H "Authorization: Bearer invalid-token"
```

## Lesson 4: Фильтрация и поиск

### Тестирование фильтров

1. Фильтрация тем:
```bash
# По имени
curl "http://127.0.0.1:8000/api/topics/?name=Test" \
     -H "Authorization: Bearer your-token"

# По описанию
curl "http://127.0.0.1:8000/api/topics/?description=Test" \
     -H "Authorization: Bearer your-token"
```

2. Фильтрация проектов:
```bash
# По теме
curl "http://127.0.0.1:8000/api/projects/?topic=1" \
     -H "Authorization: Bearer your-token"

# По названию
curl "http://127.0.0.1:8000/api/projects/?name=Test" \
     -H "Authorization: Bearer your-token"
```

3. Фильтрация задач:
```bash
# По проекту
curl "http://127.0.0.1:8000/api/tasks/?project=1" \
     -H "Authorization: Bearer your-token"

# По статусу
curl "http://127.0.0.1:8000/api/tasks/?status=new" \
     -H "Authorization: Bearer your-token"

# По исполнителю
curl "http://127.0.0.1:8000/api/tasks/?assigned_to=1" \
     -H "Authorization: Bearer your-token"
```

### Тестирование поиска

1. Поиск по названию:
```bash
curl "http://127.0.0.1:8000/api/topics/?search=Test" \
     -H "Authorization: Bearer your-token"
```

2. Поиск по описанию:
```bash
curl "http://127.0.0.1:8000/api/projects/?search=Description" \
     -H "Authorization: Bearer your-token"
```

## Lesson 5: Оптимизация

### Тестирование кэширования

1. Проверка кэширования запросов:
```bash
# Первый запрос (должен быть медленнее)
time curl http://127.0.0.1:8000/api/topics/ \
     -H "Authorization: Bearer your-token"

# Второй запрос (должен быть быстрее)
time curl http://127.0.0.1:8000/api/topics/ \
     -H "Authorization: Bearer your-token"
```

2. Проверка инвалидации кэша:
```bash
# Создание новой темы
curl -X POST http://127.0.0.1:8000/api/topics/ \
     -H "Authorization: Bearer your-token" \
     -H "Content-Type: application/json" \
     -d '{"name":"New Topic","description":"New Description"}'

# Проверка, что новая тема появилась в списке
curl http://127.0.0.1:8000/api/topics/ \
     -H "Authorization: Bearer your-token"
```

### Тестирование оптимизации запросов

1. Проверка количества запросов:
```bash
python manage.py shell

from django.db import connection
from django.db import reset_queries
from core.models import Project

# Сброс счетчика запросов
reset_queries()

# Получение проектов с задачами
projects = Project.objects.prefetch_related('tasks').all()
for project in projects:
    print(f"Project: {project.name}")
    for task in project.tasks.all():
        print(f"  Task: {task.title}")

# Вывод количества запросов
print(f"Number of queries: {len(connection.queries)}")
```

## Lesson 6: Тестирование

### Запуск тестов

1. Запуск всех тестов:
```bash
python manage.py test
```

2. Запуск конкретных тестов:
```bash
# Тесты моделей
python manage.py test core.tests.test_models

# Тесты API
python manage.py test core.tests.test_api

# Тесты аутентификации
python manage.py test core.tests.test_auth
```

3. Запуск тестов с покрытием:
```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Проверка тестового покрытия

1. Откройте отчет о покрытии:
```bash
# Откройте файл htmlcov/index.html в браузере
```

2. Проверьте покрытие для каждого модуля:
- models.py
- views.py
- serializers.py
- urls.py

## Lesson 7: Документация API

### Тестирование Swagger UI

1. Откройте Swagger UI:
- Перейдите по адресу http://127.0.0.1:8000/
- Проверьте авторизацию через Swagger UI
- Проверьте все эндпоинты через Swagger UI

2. Проверьте документацию:
- Описания всех эндпоинтов
- Параметры запросов
- Примеры ответов
- Схемы данных

### Тестирование ReDoc

1. Откройте ReDoc:
- Перейдите по адресу http://127.0.0.1:8000/redoc/
- Проверьте читаемость документации
- Проверьте навигацию по разделам

## Lesson 8: Безопасность

### Тестирование безопасности

1. Проверка CORS:
```bash
# Запрос с другого домена
curl -H "Origin: http://example.com" \
     -H "Access-Control-Request-Method: GET" \
     http://127.0.0.1:8000/api/topics/
```

2. Проверка rate limiting:
```bash
# Множественные запросы
for i in {1..100}; do
    curl http://127.0.0.1:8000/api/topics/ \
         -H "Authorization: Bearer your-token"
done
```

3. Проверка валидации данных:
```bash
# Отправка неверных данных
curl -X POST http://127.0.0.1:8000/api/topics/ \
     -H "Authorization: Bearer your-token" \
     -H "Content-Type: application/json" \
     -d '{"name":""}'
```

## Lesson 9: Мониторинг

### Тестирование логирования

1. Проверка логов:
```bash
# Проверка логов приложения
tail -f /var/log/unidoc/app.log

# Проверка логов Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Проверка логов Gunicorn
tail -f /var/log/gunicorn/access.log
tail -f /var/log/gunicorn/error.log
```

2. Проверка метрик:
```bash
# Проверка метрик Prometheus
curl http://localhost:9090/metrics

# Проверка метрик Node Exporter
curl http://localhost:9100/metrics
```

### Тестирование Grafana

1. Откройте Grafana:
- Перейдите по адресу http://localhost:3000
- Войдите с учетными данными admin/admin
- Проверьте дашборды
- Проверьте алерты

## Lesson 10: Деплой

### Тестирование production

1. Проверка SSL:
```bash
# Проверка SSL-сертификата
curl -vI https://your-domain.com

# Проверка HSTS
curl -I https://your-domain.com
```

2. Проверка бэкапов:
```bash
# Запуск бэкапа вручную
sudo /usr/local/bin/backup-unidoc.sh

# Проверка бэкапа
ls -l /var/backups/unidoc/
```

3. Проверка восстановления:
```bash
# Восстановление из бэкапа
sudo /usr/local/bin/restore-unidoc.sh 2025-05-07_00-00-00
```

### Тестирование обновления

1. Проверка обновления:
```bash
# Запуск обновления вручную
sudo /usr/local/bin/update-unidoc.sh

# Проверка статуса
sudo systemctl status gunicorn
```

2. Проверка отката:
```bash
# Восстановление предыдущей версии
git reset --hard HEAD^
sudo /usr/local/bin/update-unidoc.sh
``` 