import multiprocessing

# Количество воркеров
workers = multiprocessing.cpu_count() * 2 + 1

# Путь к WSGI приложению
wsgi_app = "password_generator:application"

# Настройки воркеров
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Настройки логирования
accesslog = "access.log"
errorlog = "error.log"
loglevel = "info"

# Настройки привязки
bind = "127.0.0.1:8000"

# Настройки перезагрузки
reload = True
reload_extra_files = ["password_generator.py"] 