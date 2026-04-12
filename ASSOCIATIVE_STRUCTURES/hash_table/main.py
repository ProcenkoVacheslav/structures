from typing import Any


class HashTable:
    def __init__(self, size: int) -> None:
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0

    def put(self, key: Any, value: Any) -> None:
        index = self.__hash(key)
        bucket = self.table[index]

        for element_id, (cur_key, cur_value) in enumerate(bucket):
            if cur_key == key:
                bucket[element_id] = (key, value)
                return

        bucket.append((key, value))
        self.count += 1

        if self.load_factor() > 0.7:
            self.__rehash()

    def get(self, key: Any, default: Any = None) -> Any:
        index = self.__hash(key)
        bucket = self.table[index]

        for cur_key, cur_value in bucket:
            if cur_key == key:
                return cur_value

        return default

    def delete(self, key: Any) -> bool:
        index = self.__hash(key)
        bucket = self.table[index]

        for element_id, (cur_key, cur_value) in enumerate(bucket):
            if cur_key == key:
                del bucket[element_id]
                self.count -= 1
                return True

        return False

    def load_factor(self):
        return self.count / self.size

    def keys(self) -> list:
        result = []
        for bucket in self.table:
            for key, value in bucket:
                result.append(key)
        return result

    def values(self) -> list:
        result = []
        for bucket in self.table:
            for key, value in bucket:
                result.append(value)
        return result

    def items(self) -> list:
        result = []
        for bucket in self.table:
            for item in bucket:
                result.append(item)
        return result

    def __hash(self, key: Any) -> int:
        if isinstance(key, str):
            return sum(ord(char) for char in key) % self.size
        elif isinstance(key, (int, float)):
            return (key * 31) % self.size
        else:
            return hash(key) % self.size

    def __rehash(self) -> None:
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0

        for bucket in old_table:
            for key, value in bucket:
                self.put(key, value)

    def __setitem__(self, key: Any, value: Any) -> None:
        self.put(key, value)

    def __getitem__(self, key: Any) -> Any:
        value = self.get(key)
        if value is None:
            raise KeyError(f"Key '{key}' not found")
        return value

    def __contains__(self, key: Any) -> bool:
        return self.get(key) is not None

    def __str__(self) -> str:
        items = []
        for bucket in self.table:
            for key, value in bucket:
                items.append(f"{key}: {value}")
        return "hash_table(" + ", ".join(items) + ")"

    def __len__(self) -> int:
        return self.count


if __name__ == "__main__":
    ht = HashTable(5)

    ht.put("apple", 10)
    ht.put("banana", 20)
    ht.put("orange", 30)
    ht["grape"] = 40

    print(f"Таблица: {ht}")
    print(f"Размер: {len(ht)}")
    print(f"Коэффициент заполнения: {ht.load_factor():.2f}")

    print(f"apple -> {ht.get('apple')}")
    print(f"banana -> {ht['banana']}")
    print(f"Несуществующий ключ -> {ht.get('mango', 'Не найдено')}")

    print(f"Есть 'apple'? {'apple' in ht}")
    print(f"Есть 'mango'? {'mango' in ht}")

    ht["apple"] = 15
    print(f"После обновления: {ht}")

    print(f"Ключи: {ht.keys()}")
    print(f"Значения: {ht.values()}")
    print(f"Пары: {ht.items()}")

    small_ht = HashTable(3)
    for i in range(10):
        small_ht.put(f"key{i}", i)

    print(f"Размер таблицы: {small_ht.size}")
    print(f"Количество элементов: {len(small_ht)}")
    print(f"Коэффициент заполнения: {small_ht.load_factor():.2f}")
    print(f"Все элементы: {small_ht}")
