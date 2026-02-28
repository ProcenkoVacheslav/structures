from typing import Any
from binary_search import BinarySearchTree


class AdditionalBinaryTreeFunctions(BinarySearchTree):
    def __init__(self):
        super().__init__()

    def preorder_traversal(self) -> list:
        # Прямой обход (корень -> левый -> правый)
        result = []
        self._preorder_recursive(self._root, result)
        return result

    def postorder_traversal(self) -> list:
        # Обратный обход (левый -> правый -> корень)
        result = []
        self._postorder_recursive(self._root, result)
        return result

    def level_order_traversal(self) -> list:
        # Обход в ширину (по уровням)
        if self._root is None:
            return []

        result = []
        queue = [self._root]

        while queue:
            current = queue.pop(0)
            result.append(current.value)

            if current.left is not None:
                queue.append(current.left)
            if current.right is not None:
                queue.append(current.right)

        return result

    def height(self) -> int:
        return self._height_recursive(self._root)

    def size(self) -> int:
        return self._size

    def is_balanced(self) -> bool:
        return self._check_balanced(self._root) != -1

    def clear(self) -> None:
        self._root = None
        self._size = 0

    def get_successor(self, value: Any) -> Any:
        # Находит преемника (следующее большее значение)
        node = self.search(value)
        if node is None:
            return None

        if node.right is not None:
            return self._find_min(node.right).value

        parent = node.parent
        while parent is not None and node == parent.right:
            node = parent
            parent = parent.parent

        return parent.value if parent is not None else None

    def get_predecessor(self, value: Any) -> Any:
        # Находит предшественника (предыдущее меньшее значение)
        node = self.search(value)
        if node is None:
            return None

        if node.left is not None:
            return self._find_max(node.left).value

        parent = node.parent
        while parent is not None and node == parent.left:
            node = parent
            parent = parent.parent

        return parent.value if parent is not None else None

    def _preorder_recursive(self, node: BinarySearchTree._Node, result: list) -> None:
        if node is not None:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def _postorder_recursive(self, node: BinarySearchTree._Node, result: list) -> None:
        if node is not None:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)

    def _height_recursive(self, node: BinarySearchTree._Node) -> int:
        if node is None:
            return 0

        return 1 + max(self._height_recursive(node.left), self._height_recursive(node.right))

    def _check_balanced(self, node: BinarySearchTree._Node) -> int:
        if node is None:
            return 0

        left_height = self._check_balanced(node.left)
        if left_height == -1:
            return -1

        right_height = self._check_balanced(node.right)
        if right_height == -1:
            return -1

        if abs(left_height - right_height) > 1:
            return -1

        return max(left_height, right_height) + 1


if __name__ == "__main__":
    bst = AdditionalBinaryTreeFunctions()

    bst.insert(10)
    bst.insert(20)
    bst.insert(4)
    bst.insert(7)

    bst_node = bst.search(7)

    print(bst_node.is_leaf())
    print(bst_node.has_one_child())

    print(4 in bst)

    print(bst)
