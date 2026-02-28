from typing import Any


class BinarySearchTree:
    class _Node:
        def __init__(self, value: int) -> None:
            self.value = value
            self.left = self.right = self.parent = None

        def is_leaf(self):
            return self.left is None and self.right is None

        def has_one_child(self):
            return (self.left is None and self.right is not None) or (self.left is not None and self.right is None)

        def __repr__(self) -> str:
            return f'node({self.value})'

    def __init__(self):
        self._root = None
        self._size = 0

    def insert(self, value: int) -> None:
        new_node = self._Node(value)

        if self._root is None:
            self._root = new_node
            return

        current_node = self._root
        parent = None

        while current_node is not None:
            parent = current_node
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right

        new_node.parent = parent

        if parent.value > value:
            parent.left = new_node
        else:
            parent.right = new_node

        self._size += 1

    def search(self, value: int) -> _Node or None:
        if self.is_empty():
            raise ValueError('Cannot fined anything in empty binary tree')

        return self._search_recursive(self._root, value)

    def delete(self, value: int) -> None:
        node_to_delete = self.search(value)
        if node_to_delete is None:
            raise ValueError("Cannot delete a nonexistent object")

        self._delete_node(node_to_delete)
        self._size -= 1

    def find_min(self) -> Any:
        if self._root is None:
            raise ValueError('Cannot find min element in empty tree')

        return self._find_min(self._root).value

    def find_max(self) -> Any:
        if self._root is None:
            raise ValueError('Cannot find min element in empty tree')

        return self._find_max(self._root).value

    def is_empty(self) -> bool:
        return self._root is None

    def contains(self, value: int):
        return self.search(value) is not None

    # tree traversal

    def inorder_traversal(self) -> list:
        result = []
        self._inorder_recursive(self._root, result)

        return result

    # protected methods

    def _inorder_recursive(self, node: _Node, result: list):
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def _search_recursive(self, node: _Node or None, value: int) -> _Node or None:
        if node is None or node.value == value:
            return node

        if value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def _delete_node(self, node: _Node):
        if node.is_leaf():
            self._replace_node_in_parent(node, None)
        elif node.has_one_child():
            child = node.left if node.left is not None else node.right
            self._replace_node_in_parent(node, child)
        else:
            successor = self._find_min(node.right)
            node.value = successor.value
            self._delete_node(successor)

    def _replace_node_in_parent(self, node: _Node, new_node: _Node or None) -> None:
        if node.parent is None:
            self._root = new_node
        elif node == node.parent.left:
            node.parent.left = new_node
        else:
            node.parent.right = new_node

        if new_node is not None:
            new_node.parent = node.parent

    @staticmethod
    def _find_min(node: _Node) -> _Node:
        while node.left is not None:
            node = node.left
        return node

    @staticmethod
    def _find_max(node: _Node) -> _Node:
        while node.right is not None:
            node = node.right
        return node

    def __contains__(self, item) -> bool:
        return self.contains(item)

    def __str__(self) -> str:
        result = self.inorder_traversal()

        return f'binary_search_tree({result})'


if __name__ == "__main__":
    bst = BinarySearchTree()

    bst.insert(10)
    bst.insert(20)
    bst.insert(4)
    bst.insert(7)

    bst_node = bst.search(7)

    print(bst_node.is_leaf())
    print(bst_node.has_one_child())

    print(4 in bst)

    print(bst)
