# cache.py

class LRUCache:
    def __init__(self, capacity: int = 10) -> None:
        self.capacity = capacity
        self.cache = {}  # основной словарь для хранения ключей и значений

    def get(self, key: str) -> str:
        if key not in self.cache:
            return ''
        # Извлекаем значение и обновляем порядок, перемещая элемент в конец (наиболее недавно использованный)
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def set(self, key: str, value: str) -> None:
        # Если ключ уже есть – удаляем его, чтобы обновить порядок вставки
        if key in self.cache:
            self.cache.pop(key)
        # Если достигнута ёмкость, удаляем наименее недавно использованный элемент (первый в словаре)
        elif len(self.cache) >= self.capacity:
            oldest_key = next(iter(self.cache))
            self.cache.pop(oldest_key)
        self.cache[key] = value

    def rem(self, key: str) -> None:
        # Удаляем ключ, если он существует
        if key in self.cache:
            self.cache.pop(key)
