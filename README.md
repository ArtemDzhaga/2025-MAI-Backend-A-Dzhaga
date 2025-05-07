# UniDoc - Система управления документами для авиакомпании

## Описание проекта
UniDoc - это система управления документами, разработанная для авиакомпании. Проект реализует функционал CRM-системы с акцентом на управление документами, задачами и проектами.

## Технологии
- Python 3.11
- Django 5.1.7
- Django REST Framework 3.16.0
- PostgreSQL (для production)
- Redis (для кэширования, опционально)
- Nginx + Gunicorn (для production)
- Swagger/OpenAPI для документации API
- JWT для аутентификации
- Django CORS Headers для CORS
- Django Filter для фильтрации
- DRF Simple JWT для JWT аутентификации
- DRF Yasg для Swagger документации

## Структура проекта
```
unidoc/
├── core/                 # Основное приложение
│   ├── models.py        # Модели данных
│   ├── serializers.py   # Сериализаторы для API
│   ├── views.py         # Представления API
│   ├── urls.py          # URL-маршруты API
│   ├── tests/           # Тесты
│   └── optimizations.py # Оптимизации
├── unidoc/              # Настройки проекта
│   ├── settings.py      # Настройки Django
│   ├── settings_prod.py # Настройки для production
│   └── urls.py          # Основные URL-маршруты
├── manage.py            # Скрипт управления Django
├── requirements.txt     # Зависимости проекта
└── DEPLOY.md           # Инструкции по деплою
```

## Реализованные функции

### Аутентификация и авторизация
- JWT аутентификация с токенами доступа и обновления
- Защита API endpoints с помощью IsAuthenticated
- CORS настройки для безопасного взаимодействия с фронтендом
- Rate limiting для защиты от DDoS атак
- Безопасное хранение паролей
- Защита от брутфорс атак

### API Endpoints
- Темы (Topics)
  - CRUD операции
  - Фильтрация по имени и описанию
  - Поиск по названию
  - Сортировка по дате создания
- Проекты (Projects)
  - CRUD операции
  - Фильтрация по теме и названию
  - Получение количества задач
  - Сортировка по приоритету
- Задачи (Tasks)
  - CRUD операции
  - Фильтрация по проекту, статусу и исполнителю
  - Получение просроченных задач
  - Сортировка по дедлайну
- Подзадачи (Subtasks)
  - CRUD операции
  - Фильтрация по задаче и статусу
  - Сортировка по приоритету
- Комментарии (Comments)
  - CRUD операции
  - Фильтрация по задаче и автору
  - Сортировка по дате создания
- Документы (Documents)
  - CRUD операции
  - Версионирование документов
  - Фильтрация по проекту и задаче
  - Сортировка по дате обновления
- Шаблоны (Templates)
  - CRUD операции
  - Фильтрация по теме
  - Сортировка по названию

### Оптимизации
- Кэширование запросов с помощью Redis (опционально)
- Оптимизация ORM-запросов с помощью select_related и prefetch_related
- Массовые операции для создания и обновления
- Измерение производительности с помощью Django Debug Toolbar
- Пагинация результатов
- Оптимизация статических файлов

### Тестирование
- Unit-тесты для моделей
- API тесты с использованием APITestCase
- Тесты аутентификации
- Тесты фильтрации и поиска
- Тесты пагинации
- Тесты оптимизаций

## План запуска

### Разработка

1. Клонировать репозиторий:
```bash
git clone <repository-url>
cd unidoc
```

2. Создать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Создать файл `.env` с настройками разработки:
```bash
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Применить миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Создать суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустить сервер разработки:
```bash
python manage.py runserver
```

### Production

1. Создать файл `.env` с production настройками (см. DEPLOY.md)

2. Установить системные зависимости:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-pip python3-dev nginx postgresql postgresql-contrib redis-server

# CentOS/RHEL
sudo yum update
sudo yum install python3-pip python3-devel nginx postgresql postgresql-server redis
```

3. Настроить базу данных PostgreSQL

4. Настроить Redis для кэширования (опционально)

5. Настроить Nginx и Gunicorn

6. Настроить SSL-сертификат

7. Настроить бэкапы и мониторинг

Подробные инструкции по деплою в production смотрите в файле DEPLOY.md

## API Endpoints

### Аутентификация
- POST /api/token/ - Получение JWT токена
- POST /api/token/refresh/ - Обновление JWT токена
- POST /api/token/verify/ - Проверка JWT токена

### Темы
- GET /api/topics/ - Список тем
- POST /api/topics/ - Создание темы
- GET /api/topics/{id}/ - Детали темы
- PUT /api/topics/{id}/ - Обновление темы
- DELETE /api/topics/{id}/ - Удаление темы
- GET /api/topics/active/ - Получение активных тем

### Проекты
- GET /api/projects/ - Список проектов
- POST /api/projects/ - Создание проекта
- GET /api/projects/{id}/ - Детали проекта
- PUT /api/projects/{id}/ - Обновление проекта
- DELETE /api/projects/{id}/ - Удаление проекта
- GET /api/projects/with-tasks/ - Проекты с количеством задач

### Задачи
- GET /api/tasks/ - Список задач
- POST /api/tasks/ - Создание задачи
- GET /api/tasks/{id}/ - Детали задачи
- PUT /api/tasks/{id}/ - Обновление задачи
- DELETE /api/tasks/{id}/ - Удаление задачи
- GET /api/tasks/overdue/ - Просроченные задачи
- GET /api/tasks/by-status/{status}/ - Задачи по статусу

### Документы
- GET /api/documents/ - Список документов
- POST /api/documents/ - Создание документа
- GET /api/documents/{id}/ - Детали документа
- PUT /api/documents/{id}/ - Обновление документа
- DELETE /api/documents/{id}/ - Удаление документа
- GET /api/documents/{id}/versions/ - Версии документа

## Тестирование
```bash
# Запуск всех тестов
python manage.py test

# Запуск конкретного теста
python manage.py test core.tests.test_models
python manage.py test core.tests.test_api

# Запуск тестов с покрытием
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Документация API
- Swagger UI: http://localhost:8000/
- ReDoc: http://localhost:8000/redoc/

## Безопасность
- JWT аутентификация с токенами доступа и обновления
- CORS настройки для безопасного взаимодействия с фронтендом
- Rate limiting для защиты от DDoS атак
- Валидация данных на уровне сериализаторов
- Защита от SQL-инъекций через ORM
- XSS защита через экранирование
- SSL/TLS в production
- Безопасное хранение паролей
- Защита от CSRF атак
- Защита от брутфорс атак
- Логирование действий пользователей
- Мониторинг безопасности

## Мониторинг и логирование
- Логирование в файлы
- Мониторинг через Prometheus
- Визуализация через Grafana
- Оповещения о критических событиях
- Мониторинг производительности
- Мониторинг безопасности
- Мониторинг доступности
- Мониторинг использования ресурсов

## Бэкапы
- Автоматические бэкапы базы данных
- Бэкапы медиа-файлов
- Ротация бэкапов
- Проверка целостности бэкапов
- Восстановление из бэкапа
- Мониторинг бэкапов
- Оповещения о проблемах с бэкапами
