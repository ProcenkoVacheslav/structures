from typing import Any


class CircularLinkedList:
    class __Node:
        def __init__(self, value: Any) -> None:
            self.value = value
            self.next = None

        def __repr__(self) -> str:
            return f'node({self.value})'

    def __init__(self) -> None:
        self.__head = None
        self.__tail = None

    def add_first(self, value: Any) -> None:
        new_node = self.__Node(value)
        if self.__is_empty():
            self.__initialize(new_node)
        else:
            new_node.next = self.__head
            self.__head = new_node
            self.__tail.next = new_node

    def add_last(self, value: Any) -> None:
        new_node = self.__Node(value)
        if self.__is_empty():
            self.__initialize(new_node)
        else:
            self.__tail.next = new_node
            self.__tail = new_node
            self.__tail.next = self.__head

    def remove_first(self) -> Any:
        if self.__is_empty():
            raise ValueError('Cannot remove an element from an empty list')

        removed_value = self.__head.value

        if self.__has_one_node():
            self.__reset()
        else:
            next_node = self.__head.next
            self.__head.next = None
            self.__head = next_node
            self.__tail.next = self.__head

        return removed_value

    def remove_last(self) -> Any:
        if self.__is_empty():
            raise ValueError('Cannot remove an element from an empty list')

        removed_value = self.__tail.value

        if self.__has_one_node():
            self.__reset()
        else:
            prev = self.__get_node_before_last()

            prev.next = self.__head
            self.__tail = prev

        return removed_value

    def remove(self, value: Any) -> None:
        if self.__is_empty():
            raise ValueError('Cannot remove an element from an empty list')

        if self.__head.value == value:
            self.remove_first()
            return

        if self.__tail.value == value:
            self.remove_last()
            return

        current = self.__head
        prev = self.__head

        while current.next != self.__head:
            if current.value == value:
                prev.next = current.next
                current.next = None
                return

            prev = current
            current = current.next

        raise ValueError('Value not found in the list')

    def get_nth_from_end(self, n: Any) -> Any:
        if self.__is_empty():
            raise ValueError('LinkedList is empty')

        if n <= 0:
            raise ValueError('Invalid value of n')

        current = self.__head

        for _ in range(n):
            if current is None:
                raise ValueError('n is larger then the size of the list')

            current = current.next

        prev = self.__head

        while current != self.__head:
            current = current.next
            prev = prev.next

        return prev.value

    def reverse(self) -> None:
        if self.__is_empty() or self.__has_one_node():
            return

        prev = None
        current = self.__head

        while current != self.__head or prev is None:
            next_node = current.next
            current.next = prev

            prev = current
            current = next_node

        self.__head, self.__tail = self.__tail, self.__head

    def get_middle(self) -> Any:
        if self.__is_empty():
            raise ValueError('LinkedList is empty')

        start_flag = True

        slow = self.__head
        fast = self.__head

        while (fast != self.__head and fast.next != self.__head) or start_flag:
            start_flag = True

            slow = slow.next
            fast = fast.next.next

        return slow.value

    def __get_node_before_last(self) -> __Node or None:
        if self.__is_empty() or self.__has_one_node():
            return None

        current = self.__head

        while current.next != self.__tail:
            current = current.next

        return current

    def __has_one_node(self) -> bool:
        return (self.__head == self.__tail) and self.__head is not None

    def __reset(self) -> None:
        self.__head = self.__tail = None

    def __is_empty(self) -> bool:
        return self.__head is None

    def __initialize(self, node) -> None:
        self.__head = self.__tail = node

    def __get_all_elements(self) -> list:
        list_of_element = list()

        current = self.__head
        list_of_element.append(self.__head.value)

        while current.next != self.__head:
            current = current.next
            list_of_element.append(current.value)

        return list_of_element

    def __str__(self) -> str:
        list_of_element = list()

        if self.__has_one_node():
            list_of_element.append(self.__head.value)
            return f'linked_list({list_of_element})'

        if self.__is_empty():
            return f'linked_list({list_of_element})'

        list_of_element = self.__get_all_elements()

        return f'linked_list({list_of_element})'

    def __len__(self) -> int:
        if self.__has_one_node():
            return 1

        if self.__is_empty():
            return 0

        list_of_element = self.__get_all_elements()
        return len(list_of_element)


if __name__ == "__main__":
    cll = CircularLinkedList()

    cll.add_last(10)
    cll.add_last(20)
    cll.add_last(30)

    cll.remove(10)
    cll.remove(20)
    cll.remove(30)

    print(cll)
    print(len(cll))

    print("")
