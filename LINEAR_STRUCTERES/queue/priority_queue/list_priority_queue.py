from typing import Any


class PriorityQueueList:
    def __init__(self):
        self.__items = []

    def is_empty(self) -> bool:
        return len(self.__items) == 0

    def enqueue(self, item: Any, priority: int) -> None:
        self.__items.append((priority, item))
        self.__items.sort(key=lambda x: x[0])

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        return self.__items.pop(0)[1]

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        return self.__items[0][1]

    def __str__(self) -> str:
        return f"priority_queue({[f'{item}[p{priority}]' for priority, item in self.__items]})"

    def __len__(self) -> int:
        return len(self.__items)
