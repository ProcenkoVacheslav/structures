from time import time
from typing import Any


class LinkedListDeque:
    class __Node:
        def __init__(self, data: Any) -> None:
            self.data = data
            self.next = None
            self.prev = None

    def __init__(self) -> None:
        self.__first = None
        self.__last = None
        self._size = 0

    def is_empty(self) -> bool:
        return self._size == 0

    def add_first(self, item: Any) -> None:
        new_node = self.__Node(item)
        if self.is_empty():
            self.__first = self.__last = new_node
        else:
            new_node.next = self.__first
            self.__first.prev = new_node
            self.__first = new_node
        self._size += 1

    def add_last(self, item: Any) -> None:
        new_node = self.__Node(item)
        if self.is_empty():
            self.__first = self.__last = new_node
        else:
            new_node.prev = self.__last
            self.__last.next = new_node
            self.__last = new_node
        self._size += 1

    def remove_first(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque is empty")

        data = self.__first.data
        if self.__first == self.__last:
            self.__first = self.__last = None
        else:
            self.__first = self.__first.next
            self.__first.prev = None
        self._size -= 1

        return data

    def remove_last(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque is empty")

        data = self.__last.data
        if self.__first == self.__last:
            self.__first = self.__last = None
        else:
            self.__last = self.__last.prev
            self.__last.next = None
        self._size -= 1

        return data

    def peek_first(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque is empty")

        return self.__first.data

    def peek_last(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque is empty")

        return self.__last.data

    def __str__(self) -> str:
        items = []
        current = self.__first
        while current:
            items.append(current.data)
            current = current.next
        return f"deque({items})"

    def __len__(self) -> int:
        return self._size


if __name__ == "__main__":

    start = time()

    dq = LinkedListDeque()

    dq.add_last(10)
    dq.add_last(20)
    dq.add_first(5)
    dq.add_first(1)

    for i in range(1000000):
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

    end = time()

    print(end - start)
