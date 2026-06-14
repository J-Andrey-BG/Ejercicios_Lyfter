class Age:
    data: int

    def __init__(self, data, right_child=None, left_child=None):
        self.data = data
        self.right_child = right_child
        self.left_child = left_child


class AgeBinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, age):
        if self.root is None:
            self.root = age
        else:
            self._insert_recursive(self.root, age)

    def _insert_recursive(self, current_node, new_node):
        if new_node.data < current_node.data:
            if current_node.left_child is None:
                current_node.left_child = new_node
            else:
                self._insert_recursive(current_node.left_child, new_node)
        else:
            if current_node.right_child is None:
                current_node.right_child = new_node
            else:
                self._insert_recursive(current_node.right_child, new_node)


    def print_structure(self):
        self._print_recursive(self.root, 0)

    def _print_recursive(self, node, level):
        if node is not None:
            self._print_recursive(node.right_child, level + 1)

            spaces = "    " * level
            print(spaces + str(node.data))

            self._print_recursive(node.left_child, level + 1)


def main():
    tree = AgeBinaryTree()
    tree.insert(Age(30))
    tree.insert(Age(20))
    tree.insert(Age(40))
    tree.insert(Age(10))
    tree.insert(Age(25))
    tree.insert(Age(35))
    tree.insert(Age(50))

    print("Structure of the binary tree:")
    tree.print_structure()


if __name__ == "__main__":
    main()