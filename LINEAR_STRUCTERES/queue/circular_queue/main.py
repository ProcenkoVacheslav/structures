from typing import Any


class CircularQueue:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def is_empty(self) -> bool:
        return self.size == 0

    def is_full(self) -> bool:
        return self.size == self.capacity

    def enqueue(self, item: Any) -> None:
        if self.is_full():
            self.__resize(self.capacity * 2)

        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = item
        self.size += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Circular queue is empty")

        item = self.queue[self.front]
        self.queue[self.front] = None

        self.front = (self.front + 1) % self.capacity
        self.size -= 1

        return item

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("Circular queue is empty")

        return self.queue[self.front]

    def get_capacity(self) -> int:
        return self.capacity

    def clear(self):
        self.front = 0
        self.rear = -1
        self.size = 0
        self.queue = [None] * self.capacity

    def __resize(self, new_capacity):
        if new_capacity <= self.size:
            new_capacity = self.size + 1

        new_queue = [None] * new_capacity
        current = self.front

        for element_id in range(self.size):
            new_queue[element_id] = self.queue[current]
            current = (current + 1) % self.capacity

        self.queue = new_queue
        self.capacity = new_capacity
        self.front = 0
        self.rear = self.size - 1

    def __str__(self) -> str:
        if self.is_empty():
            return "circularQueue([])"

        elements = []
        current = self.front
        for _ in range(self.size):
            elements.append(self.queue[current])
            current = (current + 1) % self.capacity

        return f"circularQueue({elements})"

    def __len__(self) -> int:
        return self.size

    def __contains__(self, item: Any) -> bool:
        current = self.front
        for _ in range(self.size):
            if self.queue[current] == item:
                return True
            current = (current + 1) % self.capacity
        return False


if __name__ == "__main__":
    cq = CircularQueue(5)

    for i in range(1, 6):
        cq.enqueue(i)
        print(f"Добавлен {i}: {cq}")

    print(f"Текущий размер: {len(cq)}")
    print(f"Максимальная вместимость: {cq.get_capacity()}")
    print(f"Очередь заполнена: {cq.is_full()}")

    print(f"Первый элемент: {cq.peek()}")

    print("Удаление элементов:")
    for _ in range(2):
        cur_item = cq.dequeue()
        print(f"Удален {cur_item}: {cq}")

    print(f"Текущий размер: {len(cq)}")
    print(f"Очередь заполнена: {cq.is_full()}")

    print("Добавление новых элементов (демонстрация кольцевого поведения):")
    cq.enqueue(6)
    cq.enqueue(7)
    print(f"После добавления 6 и 7: {cq}")

    print(f"Элемент 4 в очереди: {4 in cq}")
    print(f"Элемент 10 в очереди: {10 in cq}")

    print("Очистка очереди:")
    cq.clear()
    print(f"После очистки: {cq}")
    print(f"Очередь пуста: {cq.is_empty()}")
