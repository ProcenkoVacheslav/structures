from typing import Any


class Stack:
    def __init__(self) -> None:
        self.__list = list()

    def push(self, element) -> None:
        self.__list.append(element)

    def get(self) -> Any:
        if not self.is_empty():
            return self.__list.pop()

        raise IndexError('stack is empty')

    def is_empty(self) -> bool:
        return len(self.__list) == 0

    def peek(self) -> Any:
        if not self.is_empty():
            return self.__list[-1]

        raise IndexError('stack is empty')

    def __str__(self) -> str:
        return f'stack({str(self.__list)})'

    def __len__(self) -> int:
        return len(self.__list)


if __name__ == "__main__":
    stack = Stack()

    stack.push(1)
    stack.push(2)
    stack.push(3)

    print(stack)
