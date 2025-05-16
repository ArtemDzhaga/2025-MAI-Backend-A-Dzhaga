from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int = 10) -> None:
        """
        Инициализация LRU кэша с заданной емкостью
        Args:
            capacity (int): Максимальное количество элементов, которые могут храниться в кэше
        """
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: str) -> str:
        """
        Получить значение из кэша по ключу
        Args:
            key (str): Ключ для получения значения
        Returns:
            str: Значение для ключа или пустая строка, если ключ не существует
        """
        if key not in self.cache:
            return ''
        
        # Перемещаем использованный ключ в конец (наиболее недавно использованный)
        self.cache.move_to_end(key)
        return self.cache[key]

    def set(self, key: str, value: str) -> None:
        """
        Установить значение в кэше для заданного ключа
        Args:
            key (str): Ключ для установки значения
            value (str): Значение для установки
        """
        # Если ключ существует, удаляем его для обновления позиции
        if key in self.cache:
            self.cache.pop(key)
        # Если кэш полон, удаляем наименее недавно использованный элемент (первый элемент)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        
        # Добавляем новую пару ключ-значение
        self.cache[key] = value

    def rem(self, key: str) -> None:
        """
        Удалить пару ключ-значение из кэша
        Args:
            key (str): Ключ для удаления
        """
        if key in self.cache:
            self.cache.pop(key)

def main():
    cache = LRUCache(100)
    cache.set('Jesse', 'Pinkman')
    cache.set('Walter', 'White')
    cache.set('Jesse', 'James')
    print(cache.get('Jesse'))  # вернёт 'James'
    cache.rem('Walter')
    print(cache.get('Walter'))  # вернёт ''

if __name__ == "__main__":
    main()
