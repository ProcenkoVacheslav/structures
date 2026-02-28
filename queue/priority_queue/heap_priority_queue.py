from typing import Any


class PriorityQueueHeap:
    def __init__(self) -> None:
        self.__heap = []

    def is_empty(self) -> bool:
        return len(self.__heap) == 0

    def enqueue(self, item: Any, priority: int) -> None:
        self.__heap.append((priority, item))
        self.__sift_up(len(self.__heap) - 1)

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        if len(self.__heap) == 1:
            return self.__heap.pop()[1]

        highest_priority = self.__heap[0][1]

        self.__heap[0] = self.__heap.pop()

        self.__sift_down(0)

        return highest_priority

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        return self.__heap[0][1]

    def __sift_up(self, index: int) -> None:
        parent = (index - 1) // 2

        while index > 0 and self.__heap[index][0] < self.__heap[parent][0]:
            self.__heap[index], self.__heap[parent] = self.__heap[parent], self.__heap[index]
            index = parent
            parent = (index - 1) // 2

    def __sift_down(self, index: int) -> None:
        size = len(self.__heap)

        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index

            if left_child < size and self.__heap[left_child][0] < self.__heap[smallest][0]:
                smallest = left_child

            if right_child < size and self.__heap[right_child][0] < self.__heap[smallest][0]:
                smallest = right_child

            if smallest != index:
                self.__heap[index], self.__heap[smallest] = self.__heap[smallest], self.__heap[index]
                index = smallest
            else:
                break

    def __str__(self) -> str:
        return f"priority_queue_heap({[f'{item}[p{priority}]' for priority, item in self.__heap]})"

    def __len__(self) -> int:
        return len(self.__heap)
