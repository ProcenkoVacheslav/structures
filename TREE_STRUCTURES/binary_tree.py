from collections import deque
from typing import Any, Optional, Self
from multipledispatch import dispatch


class TreeNode:
    def __init__(self, value: Any) -> None:
        self.left = None
        self.right = None
        self.value = value

    def __str__(self):
        return f'TreeNode({self.value})'


class BinaryTree:
    def __init__(self, value: Optional[int | list[int]]) -> None:
        self._root = None
        self._create_root(value)
        self._current = 0
        self._depth = 0

    def __str__(self) -> str:
        if self._root is None:
            return 'BinaryTree([])'

        result = self._get_items()

        return f'BinaryTree({result})'

    def __iter__(self) -> Self:
        self._current = 0
        return self

    def __next__(self) -> int:
        items = self._get_items()
        if self._current < len(items):
            cur_value = items[self._current]
            self._current += 1
            return cur_value
        else:
            raise StopIteration

    def __len__(self) -> int:
        return self.size()

    def _get_items(self) -> list[int]:
        result = []
        queue = deque([self._root])

        while queue:
            node = queue.popleft()
            result.append(node.value)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    def _add_recursive(self, node: TreeNode, value: int) -> None:
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._add_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._add_recursive(node.right, value)

    def _create_root(self, value: Optional[int | list[int]]) -> None:
        if value is None:
            return

        if type(value) == int:
            self._root = TreeNode(value)
            return

        self._root = TreeNode(value[0])
        for cur_value in value[1:]:
            self.append(cur_value)

    def _find_min(self) -> TreeNode:
        current = self._root

        while current.left:
            current = current.left

        return current

    def _find_max(self) -> TreeNode:
        current = self._root

        while current.right:
            current = current.right

        return current

    def _fined(self, value: int) -> tuple[TreeNode, TreeNode]:
        parent = None
        current = self._root

        while current.value != value:
            if value > current.value:
                parent = current
                current = current.right
            elif value < current.value:
                parent = current
                current = current.left

        return parent, current

    def _recursive_size(self, node: TreeNode, level: int) -> int:
        if node.left is None and node.right is None:
            return level

        left_size = 0
        right_size = 0

        if node.left:
            left_size = self._recursive_size(node.left, level + 1)
        if node.right:
            right_size = self._recursive_size(node.right, level + 1)

        return max(left_size, right_size)

    def _preorder_recursive(self, node: TreeNode, result: list[int]) -> list[int]:
        result.append(node.value)

        if node.left:
            result = self._preorder_recursive(node.left, result)
        if node.right:
            result = self._preorder_recursive(node.right, result)

        return result

    def _inorder_recursive(self, node: TreeNode, result: list[int]) -> list[int]:
        if node.left is not None:
            result = self._inorder_recursive(node.left, result)

        result.append(node.value)

        if node.right is not None:
            result = self._inorder_recursive(node.right, result)

        return result

    def _postorder_recursive(self, node: TreeNode, result: list[int]) -> list[int]:

        if node.left is not None:
            result = self._postorder_recursive(node.left, result)
        if node.right is not None:
            result = self._postorder_recursive(node.right, result)

        result.append(node.value)

        return result

    def min(self) -> int:
        node = self._find_min()
        return node.value

    def max(self) -> int:
        node = self._find_max()
        return node.value

    def append(self, value: int) -> None:
        if self._root is None:
            self._root = TreeNode(value)
        else:
            self._add_recursive(self._root, value)

    def delete(self, value: int) -> None:
        if self._root.value == value:
            self._root = None
            return

        parent_node, cur_node = self._fined(value)

        if cur_node.left is None and cur_node.right is None:
            if cur_node.value > parent_node.value:
                parent_node.right = None
            else:
                parent_node.left = None

    def size(self) -> int:
        items = self._get_items()
        return len(items)

    def height(self) -> int:
        if self.is_empty():
            return 0

        return self._recursive_size(self._root, 1)

    def depth(self, node) -> int:
        return self._recursive_size(node, 1)

    def is_empty(self) -> bool:
        if self._root is None:
            return True
        return False

    @dispatch(int)
    def is_leaf(self, value: int) -> bool:
        _, current = self._fined(value)
        if current.left is None and current.right is None:
            return True

        return False

    @dispatch(TreeNode)
    def is_leaf(self, node: TreeNode) -> bool:
        return node.left is None and node.right is None

    def search(self, value: int) -> TreeNode:
        _, current = self._fined(value)
        return current

    def preorder(self) -> list[int]:
        return self._preorder_recursive(self._root, [])

    def inorder(self) -> list[int]:
        return self._inorder_recursive(self._root, [])

    def postorder(self) -> list[int]:
        return self._postorder_recursive(self._root, [])

    def level_order(self) -> list[int]:
        return self._get_items()


if __name__ == "__main__":
    tree = BinaryTree([2, 1, 6, 4, 8, 3, 5, 10, 20, 15])

    print(tree)
    print(f'минимальное - {tree.min()}')
    print(f'максимальное - {tree.max()}')
    print(f'высота - {tree.height()}')
    print(f'кол-во элементов - {len(tree)}')

    depth_node = tree.search(8)
    print(depth_node)
    print(f'Глубина узла {depth_node.value} - {tree.depth(depth_node)}')

    for element in tree:
        print(element, end=' ')
    print()

    tree.delete(3)

    print(tree)
    print('------------------')
    print(f'preorder - {tree.preorder()}')
    print(f'inorder - {tree.inorder()}')
    print(f'postorder - {tree.postorder()}')
    print(f'level_order - {tree.level_order()}')
