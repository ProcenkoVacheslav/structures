from typing import Any


class Queue:
    def __init__(self) -> None:
        self.__list = list()

    def push(self, element) -> None:
        self.__list.append(element)

    def get(self) -> Any:
        if not self.is_empty():
            return self.__list.pop(0)

    def is_empty(self) -> bool:
        return len(self.__list) == 0

    def peek(self) -> Any:
        if not self.is_empty():
            return self.__list[0]

    def __str__(self) -> str:
        return f'queue({self.__list})'

    def __len__(self) -> int:
        return len(self.__list)


queue = Queue()
queue.push(1)
queue.push(2)
queue.push(3)

print(len(queue))
print(queue)
print(queue.peek())
print(queue.is_empty())

print(queue.get())
print(queue.get())
print(queue.get())

print(queue.is_empty())
