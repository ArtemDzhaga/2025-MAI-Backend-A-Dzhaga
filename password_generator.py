import random
import string
from wsgiref.simple_server import make_server

def generate_password():
    """Генерация пароля, удовлетворяющего требованиям"""
    # Определяем наборы символов
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = '#[]().,!@&^%*'
    
    # Генерируем длину пароля (от 8 до 16)
    length = random.randint(8, 16)
    
    # Гарантируем наличие всех требуемых типов символов
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Добавляем остальные символы
    all_chars = lowercase + uppercase + digits + special
    password.extend(random.choice(all_chars) for _ in range(length - 4))
    
    # Перемешиваем пароль
    random.shuffle(password)
    return ''.join(password)

def application(environ, start_response):
    """WSGI приложение"""
    # Генерируем пароль
    password = generate_password()
    
    # Формируем ответ
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    
    return [password.encode()]

if __name__ == '__main__':
    # Запуск сервера для тестирования
    with make_server('', 8000, application) as httpd:
        print("Сервер запущен на порту 8000...")
        httpd.serve_forever() 