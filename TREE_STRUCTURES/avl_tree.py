from collections import deque
from typing import Optional, Self


class TreeNode:
    def __init__(self, value: int):
        self.left = None
        self.right = None
        self.value = value
        self.height = 1

    def __str__(self) -> str:
        return f'TreeNode({self.value})'


class AVLTree:
    def __init__(self, value: Optional[int | list[int]] = None) -> None:
        self._root = None
        self._create_tree(value)
        self._current = 0

    def __str__(self):
        if self._root is None:
            return 'AVLTree([])'
        result = self._get_items()
        return f'AVLTree({result})'

    def __len__(self):
        result = self._get_items()
        return len(result)

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

    def _create_tree(self, value: Optional[int | list[int]]):
        if value is not None:
            if isinstance(value, int):
                self._create_root(value)
            else:
                self._create_full_tree(value)

    def _create_root(self, value: int):
        self._root = TreeNode(value)

    def _create_full_tree(self, value: list[int]):
        for number in value:
            self.append(number)

    @staticmethod
    def _node_height(node: Optional[TreeNode]) -> int:
        return node.height if node else 0

    def _get_balance(self, node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        return self._node_height(node.left) - self._node_height(node.right)

    def _rotate_right(self, y: TreeNode) -> TreeNode:
        """Малый правый поворот"""
        x = y.left
        t2 = x.right

        x.right = y
        y.left = t2

        y.height = 1 + max(self._node_height(y.left), self._node_height(y.right))
        x.height = 1 + max(self._node_height(x.left), self._node_height(x.right))

        return x

    def _rotate_left(self, x: TreeNode) -> TreeNode:
        """Малый левый поворот"""
        y = x.right
        t2 = y.left

        y.left = x
        x.right = t2

        x.height = 1 + max(self._node_height(x.left), self._node_height(x.right))
        y.height = 1 + max(self._node_height(y.left), self._node_height(y.right))

        return y

    def _append_recursive(self, node: Optional[TreeNode], value: int) -> TreeNode:
        if node is None:
            return TreeNode(value)

        if value < node.value:
            node.left = self._append_recursive(node.left, value)
        elif value > node.value:
            node.right = self._append_recursive(node.right, value)
        else:
            return node

        node.height = 1 + max(self._node_height(node.left), self._node_height(node.right))

        balance = self._get_balance(node)

        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)

        if balance < -1 and value > node.right.value:
            return self._rotate_left(node)

        if balance > 1 and value > node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def append(self, value: int):
        self._root = self._append_recursive(self._root, value)

    def _get_items(self) -> list[int]:
        if self._root is None:
            return []
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

    def _preorder_recursive(self, node: TreeNode, result: list[int]) -> list[int]:
        if not node:
            return result
        result.append(node.value)
        if node.left:
            result = self._preorder_recursive(node.left, result)
        if node.right:
            result = self._preorder_recursive(node.right, result)
        return result

    def _inorder_recursive(self, node: TreeNode, result: list[int]) -> list[int]:
        if not node:
            return result
        if node.left is not None:
            result = self._inorder_recursive(node.left, result)
        result.append(node.value)
        if node.right is not None:
            result = self._inorder_recursive(node.right, result)
        return result

    def _postorder_recursive(self, node: TreeNode, result: list[int]) -> list[int]:
        if not node:
            return result
        if node.left is not None:
            result = self._postorder_recursive(node.left, result)
        if node.right is not None:
            result = self._postorder_recursive(node.right, result)
        result.append(node.value)
        return result

    @staticmethod
    def _get_min_value_node(node: TreeNode) -> TreeNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _delete_recursive(self, node: Optional[TreeNode], value: int) -> Optional[TreeNode]:
        if node is None:
            return node

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            temp = self._get_min_value_node(node.right)

            node.value = temp.value

            node.right = self._delete_recursive(node.right, temp.value)

        if node is None:
            return node

        node.height = 1 + max(self._node_height(node.left), self._node_height(node.right))

        balance = self._get_balance(node)

        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def delete(self, value: int):
        self._root = self._delete_recursive(self._root, value)

    def search(self, value: int):
        cur_node = self._root
        while cur_node and cur_node.value != value:
            if value > cur_node.value:
                cur_node = cur_node.right
            else:
                cur_node = cur_node.left
        return cur_node

    def height(self):
        return self._node_height(self._root)

    def preorder(self) -> list[int]:
        return self._preorder_recursive(self._root, [])

    def inorder(self) -> list[int]:
        return self._inorder_recursive(self._root, [])

    def postorder(self) -> list[int]:
        return self._postorder_recursive(self._root, [])

    def level_order(self) -> list[int]:
        return self._get_items()


if __name__ == "__main__":
    avl_tree = AVLTree([10, 8, 7, 6, 5])

    print(avl_tree)

    new_node = avl_tree.search(7)
    print(f'FINED NODE:\t {new_node}')

    avl_tree.delete(7)
    print(avl_tree)

    print(f'HEIGHT of tree:\t {avl_tree.height()}')

    print(f'PREORDER TRAVERSAL:\t {avl_tree.preorder()}')
    print(f'INORDER TRAVERSAL:\t {avl_tree.inorder()}')
    print(f'POSTORDER TRAVERSAL:\t {avl_tree.postorder()}')
    print(f'LEVEL ORDER TRAVERSAL:\t {avl_tree.level_order()}')
