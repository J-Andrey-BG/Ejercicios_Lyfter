class Book:
    data:str

    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class BooksStack:
    def __init__(self):
        self.top = None

    def push(self, book):
        book.next = self.top
        self.top = book

    def pop(self):
        if self.top is None:
            return None
        book = self.top
        self.top = self.top.next
        book.next = None
        return book

    def is_empty(self):
        return self.top is None

    def print_structure(self):
        current = self.top
        while current is not None:
            print(current.data)
            current = current.next


def main():
    stack = BooksStack()
    stack.push(Book("Book 1"))
    stack.push(Book("Book 2"))
    stack.push(Book("Book 3"))

    stack.print_structure()


if __name__ == "__main__":
    main()