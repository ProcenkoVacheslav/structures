from time import time
from typing import Any


class Deque:
    def __init__(self) -> None:
        self.__list = []

    def is_empty(self) -> bool:
        return len(self.__list) == 0

    def add_first(self, item: Any) -> None:
        self.__list.insert(0, item)

    def add_last(self, item: Any) -> None:
        self.__list.append(item)

    def remove_first(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque is empty")

        return self.__list.pop(0)

    def remove_last(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque is empty")

        return self.__list.pop()

    def peek_first(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self.__list[0]

    def peek_last(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self.__list[-1]

    def __str__(self) -> str:
        return f"deque({self.__list})"

    def __len__(self) -> int:
        return len(self.__list)

    def __contains__(self, item: Any) -> bool:
        return item in self.__list


if __name__ == "__main__":
    start = time()

    dq = Deque()

    dq.add_last(10)
    dq.add_last(20)
    dq.add_first(5)
    dq.add_first(1)

    for i in range(100000):
        dq.add_first((i + 1) * 382)

    print(f"Очередь: {dq}")
    print(f"Размер: {len(dq)}")

    print(f"Первый элемент: {dq.peek_first()}")
    print(f"Последний элемент: {dq.peek_last()}")

    print(f"Удален из начала: {dq.remove_first()}")
    print(f"Удален из конца: {dq.remove_last()}")

    print(f"Очередь после удалений: {dq}")
    print(f"Размер: {len(dq)}")

    print(f"Очередь пуста: {dq.is_empty()}")

    print(f"Элемент 5 в очереди: {5 in dq}")
    print(f"Элемент 15 в очереди: {15 in dq}")

    end = time()

    print(end - start)
