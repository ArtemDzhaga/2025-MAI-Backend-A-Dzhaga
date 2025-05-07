# Инструкция по деплою UniDoc

## Подготовка к деплою

1. Создайте файл `.env` в корневой директории проекта:
```bash
# Основные настройки Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Настройки базы данных
DB_NAME=unidoc
DB_USER=unidoc_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Настройки Redis (опционально)
REDIS_URL=redis://localhost:6379/1

# Настройки почты
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Настройки CORS
CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# Настройки безопасности
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS=DENY
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Настройки кэширования
CACHE_TTL=300
CACHE_KEY_PREFIX=unidoc_

# Настройки логирования
LOG_LEVEL=INFO
LOG_FILE=/var/log/unidoc/app.log
```

2. Установите необходимые системные зависимости:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    nginx \
    postgresql \
    postgresql-contrib \
    redis-server \
    supervisor \
    certbot \
    python3-certbot-nginx \
    ufw \
    fail2ban

# CentOS/RHEL
sudo yum update
sudo yum install -y \
    python3-pip \
    python3-devel \
    nginx \
    postgresql \
    postgresql-server \
    redis \
    supervisor \
    certbot \
    python3-certbot-nginx \
    firewalld \
    fail2ban
```

3. Настройте файрвол:
```bash
# Ubuntu/Debian
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

4. Настройте fail2ban:
```bash
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local

# Добавьте следующие настройки:
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3
bantime = 3600

sudo systemctl restart fail2ban
```

## Настройка базы данных

1. Создайте базу данных и пользователя:
```bash
sudo -u postgres psql

# В консоли PostgreSQL:
CREATE DATABASE unidoc;
CREATE USER unidoc_user WITH PASSWORD 'your-password';
ALTER ROLE unidoc_user SET client_encoding TO 'utf8';
ALTER ROLE unidoc_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE unidoc_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE unidoc TO unidoc_user;
\q
```

2. Настройте PostgreSQL для безопасности:
```bash
sudo nano /etc/postgresql/13/main/postgresql.conf

# Добавьте или измените следующие параметры:
listen_addresses = 'localhost'
max_connections = 100
shared_buffers = 128MB
work_mem = 4MB
maintenance_work_mem = 64MB
effective_cache_size = 4GB
log_min_duration_statement = 250
log_connections = on
log_disconnections = on
log_duration = on
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
log_statement = 'ddl'
log_temp_files = 0
log_autovacuum_min_duration = 0
track_activities = on
track_counts = on
track_io_timing = on
track_functions = all
track_activity_query_size = 2048

sudo nano /etc/postgresql/13/main/pg_hba.conf

# Добавьте следующие строки:
local   all             postgres                                peer
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
host    unidoc          unidoc_user     127.0.0.1/32            md5
```

3. Перезапустите PostgreSQL:
```bash
sudo systemctl restart postgresql
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

6. Создайте индексы:
```bash
python manage.py sqlmigrate core 0001
```

7. Настройте бэкапы базы данных:
```bash
sudo mkdir -p /var/backups/unidoc
sudo chown postgres:postgres /var/backups/unidoc

# Создайте скрипт для бэкапа
sudo nano /usr/local/bin/backup-unidoc.sh

#!/bin/bash
BACKUP_DIR="/var/backups/unidoc"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
DB_NAME="unidoc"
DB_USER="unidoc_user"

# Бэкап базы данных
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Удаление старых бэкапов (старше 30 дней)
find $BACKUP_DIR -type f -mtime +30 -delete

# Проверка целостности бэкапа
gunzip -t $BACKUP_DIR/db_$DATE.sql.gz

# Отправка уведомления
if [ $? -eq 0 ]; then
    echo "Backup completed successfully: $BACKUP_DIR/db_$DATE.sql.gz" | mail -s "UniDoc Backup Success" admin@your-domain.com
else
    echo "Backup failed!" | mail -s "UniDoc Backup Failed" admin@your-domain.com
fi

sudo chmod +x /usr/local/bin/backup-unidoc.sh

# Добавьте в crontab
sudo crontab -e

# Добавьте строку:
0 0 * * * /usr/local/bin/backup-unidoc.sh
```

## Настройка Gunicorn

1. Создайте файл `gunicorn.service`:
```ini
[Unit]
Description=Gunicorn daemon for UniDoc
After=network.target postgresql.service redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/unidoc
Environment="PATH=/path/to/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=unidoc.settings_prod"
ExecStart=/path/to/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/path/to/unidoc/unidoc.sock \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    --capture-output \
    --log-level info \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --worker-class gthread \
    --threads 3 \
    unidoc.wsgi:application

[Install]
WantedBy=multi-user.target
```

2. Создайте директории для логов:
```bash
sudo mkdir -p /var/log/gunicorn
sudo chown -R www-data:www-data /var/log/gunicorn
```

3. Запустите Gunicorn:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

4. Проверьте статус:
```bash
sudo systemctl status gunicorn
```

## Настройка Nginx

1. Создайте конфигурацию Nginx:
```nginx
# /etc/nginx/sites-available/unidoc
upstream unidoc {
    server unix:/path/to/unidoc/unidoc.sock fail_timeout=0;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    add_header Strict-Transport-Security "max-age=63072000" always;

    client_max_body_size 10M;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;

    access_log /var/log/nginx/unidoc.access.log;
    error_log /var/log/nginx/unidoc.error.log;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }

    location /static/ {
        alias /path/to/unidoc/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location /media/ {
        alias /path/to/unidoc/media/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_buffering off;
        proxy_pass http://unidoc;
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
        proxy_send_timeout 60s;
    }

    # Запрет доступа к скрытым файлам
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

2. Активируйте конфигурацию:
```bash
sudo ln -s /etc/nginx/sites-available/unidoc /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

3. Настройте логирование:
```bash
sudo nano /etc/logrotate.d/nginx

# Добавьте следующие строки:
/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    sharedscripts
    prerotate
        if [ -d /etc/logrotate.d/httpd-prerotate ]; then \
            run-parts /etc/logrotate.d/httpd-prerotate; \
        fi \
    endscript
    postrotate
        invoke-rc.d nginx rotate >/dev/null 2>&1
    endscript
}
```

## Настройка SSL

1. Установите Certbot:
```bash
sudo apt-get install certbot python3-certbot-nginx
```

2. Получите SSL-сертификат:
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

3. Настройте автоматическое обновление:
```bash
sudo certbot renew --dry-run
sudo crontab -e

# Добавьте строку:
0 0 1 * * certbot renew --quiet
```

## Настройка мониторинга

1. Установите и настройте Prometheus:
```bash
wget https://github.com/prometheus/prometheus/releases/download/v2.30.0/prometheus-2.30.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*

# Создайте конфигурацию
cat > prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'unidoc'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scheme: 'http'

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
EOF

# Создайте systemd сервис
sudo nano /etc/systemd/system/prometheus.service

[Unit]
Description=Prometheus
After=network.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
    --config.file /etc/prometheus/prometheus.yml \
    --storage.tsdb.path /var/lib/prometheus \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target

sudo systemctl start prometheus
sudo systemctl enable prometheus
```

2. Установите и настройте Grafana:
```bash
wget https://dl.grafana.com/oss/release/grafana_8.2.0_amd64.deb
sudo dpkg -i grafana_8.2.0_amd64.deb

sudo nano /etc/grafana/grafana.ini

# Измените следующие параметры:
[security]
admin_user = admin
admin_password = your-secure-password
disable_initial_admin_creation = false

[server]
http_port = 3000
domain = your-domain.com
root_url = https://your-domain.com/grafana/

sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

3. Настройте Node Exporter:
```bash
wget https://github.com/prometheus/node_exporter/releases/download/v1.2.2/node_exporter-1.2.2.linux-amd64.tar.gz
tar xvfz node_exporter-*.tar.gz
cd node_exporter-*

sudo mv node_exporter /usr/local/bin/
sudo useradd -rs /bin/false node_exporter

sudo nano /etc/systemd/system/node_exporter.service

[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target

sudo systemctl start node_exporter
sudo systemctl enable node_exporter
```

## Обновление приложения

1. Создайте скрипт для обновления:
```bash
sudo nano /usr/local/bin/update-unidoc.sh

#!/bin/bash
cd /path/to/unidoc

# Остановите Gunicorn
sudo systemctl stop gunicorn

# Обновите код
git pull origin main

# Активируйте виртуальное окружение
source venv/bin/activate

# Обновите зависимости
pip install -r requirements.txt

# Примените миграции
python manage.py migrate

# Соберите статические файлы
python manage.py collectstatic --noinput

# Перезапустите Gunicorn
sudo systemctl start gunicorn

# Проверьте статус
sudo systemctl status gunicorn

# Отправьте уведомление
if [ $? -eq 0 ]; then
    echo "Update completed successfully" | mail -s "UniDoc Update Success" admin@your-domain.com
else
    echo "Update failed!" | mail -s "UniDoc Update Failed" admin@your-domain.com
fi

sudo chmod +x /usr/local/bin/update-unidoc.sh
```

2. Настройте автоматическое обновление:
```bash
sudo crontab -e

# Добавьте строку:
0 2 * * * /usr/local/bin/update-unidoc.sh
```

## Восстановление из бэкапа

1. Создайте скрипт для восстановления:
```bash
sudo nano /usr/local/bin/restore-unidoc.sh

#!/bin/bash
BACKUP_DIR="/var/backups/unidoc"
DB_NAME="unidoc"
DB_USER="unidoc_user"

# Остановите приложение
sudo systemctl stop gunicorn

# Восстановите базу данных
gunzip -c $BACKUP_DIR/db_$1.sql.gz | psql -U $DB_USER $DB_NAME

# Восстановите медиа-файлы
tar -xzf $BACKUP_DIR/media_$1.tar.gz -C /path/to/unidoc

# Перезапустите приложение
sudo systemctl start gunicorn

# Проверьте статус
sudo systemctl status gunicorn

# Отправьте уведомление
if [ $? -eq 0 ]; then
    echo "Restore completed successfully" | mail -s "UniDoc Restore Success" admin@your-domain.com
else
    echo "Restore failed!" | mail -s "UniDoc Restore Failed" admin@your-domain.com
fi

sudo chmod +x /usr/local/bin/restore-unidoc.sh
```

2. Использование скрипта восстановления:
```bash
sudo /usr/local/bin/restore-unidoc.sh 2025-05-07_00-00-00
``` 