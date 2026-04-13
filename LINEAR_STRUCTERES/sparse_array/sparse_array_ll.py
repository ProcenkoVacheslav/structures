from typing import Any, Self, Optional, Iterable


class SparseNode:
    __slots__ = ('index', 'value', 'next')

    def __init__(self, index: int, value: Any, next_node: Optional[Self] = None) -> None:
        self.index = index
        self.value = value
        self.next = next_node


class SparseLinkedListArray:
    def __init__(self, length: int, default_value=0):
        self._length = length
        self._default_value = default_value
        self._head: Optional[SparseNode] = None
        self._size = 0

    def _find_prev(self, index: int) -> tuple[Optional[SparseNode], Optional[SparseNode]]:
        prev = None
        curr = self._head
        while curr is not None and curr.index < index:
            prev = curr
            curr = curr.next
        if curr is not None and curr.index == index:
            return curr, prev
        return None, prev

    def __getitem__(self, index: int) -> Any:
        if index < 0 or index >= self._length:
            raise IndexError("Index out of range")

        node, _ = self._find_prev(index)
        if node is not None:
            return node.value
        return self._default_value

    def __setitem__(self, index: int, value) -> None:
        if index < 0 or index >= self._length:
            raise IndexError("Index out of range")

        if value == self._default_value:
            self._delete_node(index)
            return

        node, prev = self._find_prev(index)
        if node is not None:
            node.value = value
        else:
            new_node = SparseNode(index, value)
            if prev is None:
                new_node.next = self._head
                self._head = new_node
            else:
                new_node.next = prev.next
                prev.next = new_node
            self._size += 1

    def _delete_node(self, index: int) -> None:
        node, prev = self._find_prev(index)
        if node is None:
            return

        if prev is None:
            self._head = node.next
        else:
            prev.next = node.next
        self._size -= 1

    def __len__(self) -> int:
        return self._length

    def not_null_elements(self) -> int:
        return self._size

    def items(self) -> Iterable[tuple[int, any]]:
        curr = self._head
        while curr is not None:
            yield curr.index, curr.value
            curr = curr.next

    def __str__(self) -> str:
        full_repr = []
        curr = self._head
        idx = 0
        while idx < self._length:
            if curr and curr.index == idx:
                full_repr.append(str(curr.value))
                curr = curr.next
            else:
                full_repr.append(str(self._default_value))
            idx += 1
        return f"SparseLinkedListArray({full_repr})"


if __name__ == "__main__":
    sp = SparseLinkedListArray(10, default_value=0)

    sp[3] = 42
    sp[7] = 99
    sp[1] = 5
    sp[3] = 100

    print(sp[3])
    print(sp[5])

    print(len(sp))
    print(sp.not_null_elements())

    for idx_, val in sp.items():
        print(f"sp[{idx_}] = {val}")

    print(sp)

    sp[1] = 0
    print(sp.not_null_elements())
    print(sp[1])

    for idx_, val in sp.items():
        print(f"sp[{idx_}] = {val}")
