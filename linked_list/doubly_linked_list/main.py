from typing import Any


class DoublyLinkedList:
    class __Node:
        def __init__(self, value: Any) -> None:
            self.value = value
            self.prev = self.next = None

        def __repr__(self) -> str:
            return f'node({self.value})'

    def __init__(self) -> None:
        self.__head = self.__tail = None

    def add_first(self, value: Any) -> __Node:
        new_node = self.__Node(value)

        if self.__is_empty():
            self.__initialize(new_node)
        else:
            new_node.next = self.__head
            self.__head.prev = new_node
            self.__head = new_node

        return new_node

    def add_last(self, value: Any) -> __Node:
        new_node = self.__Node(value)

        if self.__is_empty():
            self.__initialize(new_node)
        else:
            new_node.prev = self.__tail
            self.__tail.next = new_node
            self.__tail = new_node
        return new_node

    def remove_fist(self) -> __Node:
        if self.__is_empty():
            raise IndexError('Cannot remove an element form an empty list')

        removed_node = self.__head

        if self.__has_one_node():
            self.__reset()
        else:
            new_head = self.__head.next
            self.__head.next = None
            new_head.prev = None
            self.__head = new_head

        return removed_node

    def remove_last(self) -> __Node:
        if self.__is_empty():
            raise IndexError('Cannot remove an element form an empty list')

        removed_node = self.__tail

        if self.__has_one_node():
            self.__reset()
        else:
            prev_node = self.__tail.prev
            self.__tail.prev = None
            prev_node.next = None
            self.__tail = prev_node

        return removed_node

    def remove(self, linked_list_object: __Node or Any) -> None:
        if self.__is_empty():
            raise IndexError('Cannot remove an element form an empty list')

        if type(linked_list_object) == self.__Node:
            self.__remove_node(linked_list_object)
        else:
            self.__remove_value(linked_list_object)

    def __remove_value(self, value: Any) -> None:

        if self.__head.value == value:
            self.remove_fist()
            return

        if self.__tail.value == value:
            self.remove_last()
            return

        current = self.__head
        prev = self.__head

        while current.next:
            if current.value == value:
                current.next = None
                prev.next = current.next
                return
            prev = prev.next
            current = current.next

        raise ValueError('Value not found in the list')

    def __remove_node(self, node: Any) -> None:
        if node == self.__head:
            self.remove_fist()
            return

        if node == self.__tail:
            self.remove_last()
            return

        prev_node = node.prev
        next_node = node.next

        node.prev = None
        node.next = None

        prev_node.next = next_node
        next_node.prev = next_node

    def __get_values(self) -> list:
        current = self.__head

        result = list()

        while current.next:
            result.append(current.value)
            current = current.next

        result.append(self.__tail.value)

        return result

    def __is_empty(self) -> bool:
        return self.__head is None

    def __has_one_node(self) -> bool:
        return (self.__head == self.__tail) and self.__head is not None

    def __initialize(self, node: __Node) -> None:
        self.__head = self.__tail = node

    def __reset(self) -> None:
        self.__head = self.__tail = None

    def __str__(self) -> str:
        result = list() if self.__is_empty() else self.__get_values()
        return f'doubly_linked_list({result})'

    def __len__(self) -> int:
        result = list() if self.__is_empty() else self.__get_values()
        return len(result)


if __name__ == "__main__":
    ll = DoublyLinkedList()

    ll.add_last(10)
    ll.add_last(20)
    ll.add_last(30)

    print(len(ll))
