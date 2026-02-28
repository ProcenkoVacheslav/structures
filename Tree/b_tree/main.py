class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.keys = []
        self.children = []
        self.leaf = leaf

    def traverse(self):
        result = []

        for i in range(len(self.keys)):
            if not self.leaf:
                result.extend(self.children[i].traverse())
            result.append(self.keys[i])

        if not self.leaf:
            result.extend(self.children[len(self.keys)].traverse())

        return result

    def search(self, k):
        i = 0
        while i < len(self.keys) and k > self.keys[i]:
            i += 1

        if i < len(self.keys) and self.keys[i] == k:
            return self

        if self.leaf:
            return None

        return self.children[i].search(k)

    def insert_non_full(self, k):
        i = len(self.keys) - 1

        if self.leaf:
            self.keys.append(0)
            while i >= 0 and self.keys[i] > k:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = k
        else:
            while i >= 0 and self.keys[i] > k:
                i -= 1

            if len(self.children[i + 1].keys) == 2 * self.t - 1:
                self._split_child(i + 1)
                if self.keys[i + 1] < k:
                    i += 1

            self.children[i + 1].insert_non_full(k)

    def _split_child(self, i):
        t = self.t
        full_child = self.children[i]
        new_child = BTreeNode(t, full_child.leaf)

        self.children.insert(i + 1, new_child)
        self.keys.insert(i, full_child.keys[t - 1])

        new_child.keys = full_child.keys[t:(2 * t - 1)]
        full_child.keys = full_child.keys[0:(t - 1)]

        if not full_child.leaf:
            new_child.children = full_child.children[t:(2 * t)]
            full_child.children = full_child.children[0:t]

    def delete(self, k):
        t = self.t

        idx = 0
        while idx < len(self.keys) and self.keys[idx] < k:
            idx += 1

        if idx < len(self.keys) and self.keys[idx] == k:
            if self.leaf:
                self.keys.pop(idx)
            else:
                self._delete_internal_node(idx)
        else:
            if self.leaf:
                return

            flag = (idx == len(self.keys))

            if len(self.children[idx].keys) < t:
                self._fill(idx)

            if flag and idx > len(self.keys):
                self.children[idx - 1].delete(k)
            else:
                self.children[idx].delete(k)

    def _delete_internal_node(self, idx):
        t = self.t
        k = self.keys[idx]

        if len(self.children[idx].keys) >= t:
            old = self._get_predecessor(idx)
            self.keys[idx] = old
            self.children[idx].delete(old)

        elif len(self.children[idx + 1].keys) >= t:
            successor = self._get_successor(idx)
            self.keys[idx] = successor
            self.children[idx + 1].delete(successor)

        else:
            self._merge(idx)
            self.children[idx].delete(k)

    def _get_predecessor(self, idx):
        current = self.children[idx]
        while not current.leaf:
            current = current.children[len(current.keys)]
        return current.keys[-1]

    def _get_successor(self, idx):
        current = self.children[idx + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    def _fill(self, idx):
        t = self.t

        if idx != 0 and len(self.children[idx - 1].keys) >= t:
            self._borrow_from_prev(idx)

        elif idx != len(self.keys) and len(self.children[idx + 1].keys) >= t:
            self._borrow_from_next(idx)

        else:
            if idx != len(self.keys):
                self._merge(idx)
            else:
                self._merge(idx - 1)

    def _borrow_from_prev(self, idx):
        child = self.children[idx]
        sibling = self.children[idx - 1]

        child.keys.insert(0, self.keys[idx - 1])

        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

        self.keys[idx - 1] = sibling.keys.pop()

    def _borrow_from_next(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys[idx])

        if not child.leaf:
            child.children.append(sibling.children.pop(0))

        self.keys[idx] = sibling.keys.pop(0)

    def _merge(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys.pop(idx))

        child.keys.extend(sibling.keys)

        if not child.leaf:
            child.children.extend(sibling.children)

        self.children.pop(idx + 1)

    def __str__(self):
        return f"Keys: {self.keys}, Leaf: {self.leaf}, Children: {len(self.children)}"


class BTree:
    def __init__(self, t):
        self.root = None
        self.t = t

    def traverse(self):
        if self.root is not None:
            return self.root.traverse()
        return []

    def search(self, k):
        return self.root.search(k) if self.root is not None else None

    def insert(self, k):
        if self.root is None:
            self.root = BTreeNode(self.t, True)
            self.root.keys.append(k)
        else:
            if len(self.root.keys) == 2 * self.t - 1:
                new_root = BTreeNode(self.t, False)
                new_root.children.append(self.root)
                self._split_child(new_root, 0)

                i = 0
                if new_root.keys[0] < k:
                    i += 1

                new_root.children[i].insert_non_full(k)

                self.root = new_root
            else:
                self.root.insert_non_full(k)

    def _split_child(self, parent, i):
        t = self.t
        full_child = parent.children[i]
        new_child = BTreeNode(t, full_child.leaf)

        parent.children.insert(i + 1, new_child)
        parent.keys.insert(i, full_child.keys[t - 1])

        new_child.keys = full_child.keys[t:(2 * t - 1)]
        full_child.keys = full_child.keys[0:(t - 1)]

        if not full_child.leaf:
            new_child.children = full_child.children[t:(2 * t)]
            full_child.children = full_child.children[0:t]

    def delete(self, k):
        if self.root is None:
            return

        self.root.delete(k)

        if len(self.root.keys) == 0:
            if self.root.leaf:
                self.root = None
            else:
                self.root = self.root.children[0]

    def __str__(self):
        return f"BTree(t={self.t}), traversal: {self.traverse()}"


if __name__ == "__main__":
    btree = BTree(3)

    keys = [10, 20, 5, 6, 12, 30, 7, 17, 3, 8, 25, 15]
    for key in keys:
        btree.insert(key)

    print(btree)

    search_keys = [12, 100, 7]
    for key in search_keys:
        cur_result = btree.search(key)

    delete_keys = [6, 15, 10]
    for key in delete_keys:
        btree.delete(key)
