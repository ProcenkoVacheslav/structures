import heapq
from typing import Any


class PriorityQueueHeapq:
    def __init__(self) -> None:
        self.__heap = []
        self.__counter = 0

    def is_empty(self) -> bool:
        return len(self.__heap) == 0

    def enqueue(self, item: Any, priority: int) -> None:
        heapq.heappush(self.__heap, (priority, self.__counter, item))
        self.__counter += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        priority, __counter, item = heapq.heappop(self.__heap)
        return item

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        return self.__heap[0][2]

    def __str__(self) -> str:
        sorted_items = sorted([(pri, cnt, item) for pri, cnt, item in self.__heap])
        return f"priority_queue_heapq({[f'{item}[p{priority}]' for priority, cnt, item in sorted_items]})"

    def __len__(self) -> int:
        return len(self.__heap)
