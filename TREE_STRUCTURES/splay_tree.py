from collections import deque
from typing import Self, Optional


class TreeNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self) -> str:
        return f'TreeNode({self.value})'


class SplayTree:
    def __init__(self, value: Optional[int | list[int]] = None) -> None:
        self._root = None

        if value:
            self._create_tree(value)

    def __str__(self) -> str:
        if self._root is None:
            return 'SplayTree([])'
        result = self._get_items()
        return f'SplayTree({result})'

    def __len__(self) -> int:
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

    def _create_tree(self, value: int | list[int]) -> None:
        if type(value) == int:
            self._root = TreeNode(value)
        else:
            for number in value:
                self.append(number)

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

    def _rotate_left(self, x: TreeNode) -> None:
        """Малое левое вращение"""
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self._root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x: TreeNode) -> None:
        """Малое правое вращение"""
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if not x.parent:
            self._root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def _splay(self, x: TreeNode) -> None:
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            elif x == p.left and p == g.left:
                self._rotate_right(g)
                self._rotate_right(p)
            elif x == x.parent.right and p == g.right:
                self._rotate_left(g)
                self._rotate_left(p)
            elif x == p.right and p == g.left:
                self._rotate_left(p)
                self._rotate_right(g)
            else:
                self._rotate_right(p)
                self._rotate_left(g)

    def append(self, value: int) -> None:
        new_node = TreeNode(value)
        if not self._root:
            self._root = new_node
            return

        curr = self._root
        parent = None
        while curr:
            parent = curr
            if value < curr.value:
                curr = curr.left
            elif value > curr.value:
                curr = curr.right
            else:
                curr.value = value
                self._splay(curr)
                return

        new_node.parent = parent
        if value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        self._splay(new_node)

    def search(self, value: int) -> Optional[TreeNode]:
        if not self._root:
            return None

        curr = self._root
        last_visited = None
        while curr:
            last_visited = curr
            if value < curr.value:
                curr = curr.left
            elif value > curr.value:
                curr = curr.right
            else:
                self._splay(curr)
                return curr

        self._splay(last_visited)
        return None

    def delete(self, value: int) -> bool:
        if not self._root:
            return False

        self.search(value)
        if self._root.value != value:
            return False

        left_tree = self._root.left
        right_tree = self._root.right

        if left_tree:
            left_tree.parent = None
        if right_tree:
            right_tree.parent = None

        if not left_tree:
            self._root = right_tree
        else:
            curr = left_tree
            while curr.right:
                curr = curr.right

            self._root = left_tree
            self._splay(curr)

            self._root.right = right_tree
            if right_tree:
                right_tree.parent = self._root
        return True


if __name__ == "__main__":
    tree = SplayTree([10, 20, 5, 15])

    node = tree.search(20)
    print(node)

    print(tree)
    print(len(tree))

    tree.delete(5)

    print(tree)
