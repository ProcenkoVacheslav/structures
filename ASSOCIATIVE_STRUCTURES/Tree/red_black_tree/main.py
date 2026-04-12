from typing import Literal, Optional

Colors = Literal['RED', 'BLACK']


class RedBlackTree:
    class __Node:
        def __init__(self, value: Optional[int], color: Colors = 'RED') -> None:
            self.value = value
            self.color = color
            self.left = None
            self.right = None
            self.parent = None

        def __repr__(self) -> str:
            return f'node({self.value})'

    def __init__(self) -> None:
        self.__NIL = self.__Node(None, 'BLACK')
        self.__root = self.__NIL

    def insert(self, value: Optional[int] = None) -> None:
        new_node = self.__Node(value, 'RED')
        new_node.left = self.__NIL
        new_node.right = self.__NIL

        parent = self.__NIL
        current = self.__root

        while current != self.__NIL:
            parent = current
            if new_node.value < current.value:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent == self.__NIL:
            self.__root = new_node
        elif new_node.value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        self.__insert_fixup(new_node)

    def search(self, value: int) -> Optional[__Node]:
        current = self.__root
        while current != self.__NIL:
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return None

    def delete(self, value: int) -> None:
        node = self.search(value)
        if node is None:
            return

        original_color = node.color
        if node.left == self.__NIL:
            x = node.right
            self.__transplant(node, node.right)
        elif node.right == self.__NIL:
            x = node.left
            self.__transplant(node, node.left)
        else:
            successor = self.__minimum(node.right)
            original_color = successor.color
            x = successor.right

            if successor.parent == node:
                x.parent = successor
            else:
                self.__transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor

            self.__transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor
            successor.color = node.color

        if original_color == 'BLACK':
            self.__delete_fixup(x)

    def inorder_traversal(self, node: Optional[__Node] = None, result: Optional[list[int]] = None) -> list[int]:
        if result is None:
            result = []
        if node is None:
            node = self.__root

        if node != self.__NIL:
            self.inorder_traversal(node.left, result)
            result.append((node.value, node.color))
            self.inorder_traversal(node.right, result)

        return result

    def height(self, node: Optional[__Node] = None) -> int:
        if node is None:
            node = self.__root
        if node == self.__NIL:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def __left_rotate(self, x: __Node) -> None:
        y = x.right
        x.right = y.left

        if y.left != self.__NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == self.__NIL:
            self.__root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def __right_rotate(self, y: __Node) -> None:
        x = y.left
        y.left = x.right

        if x.right != self.__NIL:
            x.right.parent = y

        x.parent = y.parent

        if y.parent == self.__NIL:
            self.__root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    def __insert_fixup(self, node: __Node) -> None:
        while node.parent.color == 'RED':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right

                if uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.__left_rotate(node)

                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self.__right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left

                if uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.__right_rotate(node)

                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self.__left_rotate(node.parent.parent)

        self.__root.color = 'BLACK'

    def __transplant(self, u, v) -> None:
        if u.parent == self.__NIL:
            self.__root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def __minimum(self, node) -> __Node:
        while node.left != self.__NIL:
            node = node.left
        return node

    def __delete_fixup(self, x) -> None:
        while x != self.__root and x.color == 'BLACK':
            if x == x.parent.left:
                sibling = x.parent.right

                if sibling.color == 'RED':
                    sibling.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.__left_rotate(x.parent)
                    sibling = x.parent.right

                if sibling.left.color == 'BLACK' and sibling.right.color == 'BLACK':
                    sibling.color = 'RED'
                    x = x.parent
                else:
                    if sibling.right.color == 'BLACK':
                        sibling.left.color = 'BLACK'
                        sibling.color = 'RED'
                        self.__right_rotate(sibling)
                        sibling = x.parent.right

                    sibling.color = x.parent.color
                    x.parent.color = 'BLACK'
                    sibling.right.color = 'BLACK'
                    self.__left_rotate(x.parent)
                    x = self.__root
            else:
                sibling = x.parent.left

                if sibling.color == 'RED':
                    sibling.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.__right_rotate(x.parent)
                    sibling = x.parent.left

                if sibling.right.color == 'BLACK' and sibling.left.color == 'BLACK':
                    sibling.color = 'RED'
                    x = x.parent
                else:
                    if sibling.left.color == 'BLACK':
                        sibling.right.color = 'BLACK'
                        sibling.color = 'RED'
                        self.__left_rotate(sibling)
                        sibling = x.parent.left

                    sibling.color = x.parent.color
                    x.parent.color = 'BLACK'
                    sibling.left.color = 'BLACK'
                    self.__right_rotate(x.parent)
                    x = self.__root

        x.color = 'BLACK'

    def __str__(self) -> str:
        return f'red_black_tree({self.inorder_traversal()})'


if __name__ == "__main__":
    rb_tree = RedBlackTree()

    keys = [10, 20, 30, 15, 25, 5, 35, 40, 50, 45]
    for key in keys:
        rb_tree.insert(key)

    print("Поиск 25:", "Найден" if rb_tree.search(25) else "Не найден")
    print("Поиск 100:", "Найден" if rb_tree.search(100) else "Не найден")

    print("In-order обход:", rb_tree.inorder_traversal())

    print("Высота дерева:", rb_tree.height())

    rb_tree.delete(25)
    print("После удаления 25:", rb_tree.inorder_traversal())

    print(rb_tree)
