class Wagon:
    data: str

    def __init__(self, data, next=None, previous=None):
        self.data = data
        self.previous = previous
        self.next = next


class Train:
    def __init__(self):
        self.head = None
        self.tail = None

    def push_left(self, wagon):
        wagon.previous = None
        wagon.next = self.head

        if self.head is None:
            self.tail = wagon
        else:
            self.head.previous = wagon

        self.head = wagon

    def push_right(self, wagon):
        wagon.next = None
        wagon.previous = self.tail

        if self.tail is None:
            self.head = wagon
        else:
            self.tail.next = wagon

        self.tail = wagon

    def pop_left(self):
        if self.head is None:
            return None

        wagon = self.head
        self.head = self.head.next

        if self.head is None:
            self.tail = None
        else:
            self.head.previous = None

        wagon.next = None
        wagon.previous = None

        return wagon

    def pop_right(self):
        if self.tail is None:
            return None

        wagon = self.tail
        self.tail = self.tail.previous

        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None

        wagon.next = None
        wagon.previous = None

        return wagon

    def is_empty(self):
        return self.head is None

    def print_structure(self):
        current = self.head

        while current is not None:
            print(current.data)
            current = current.next


def main():
    train = Train()
    train.push_left(Wagon("Wagon 1"))
    train.push_left(Wagon("Wagon 2"))
    train.push_right(Wagon("Wagon 3"))
    train.push_right(Wagon("Wagon 4"))
    train.push_left(Wagon("Wagon 5"))

    print("Original structure:")
    train.print_structure()

    print("\nPop left:")
    wagon = train.pop_left()
    if wagon is not None:
        print(wagon.data)

    print("\nStructure after pop_left:")
    train.print_structure()

    print("\nPop right:")
    wagon = train.pop_right()
    if wagon is not None:
        print(wagon.data)

    print("\nStructure after pop_right:")
    train.print_structure()

    print("\nPop left:")
    wagon = train.pop_left()
    if wagon is not None:
        print(wagon.data)

    print("\nStructure after pop_left:")
    train.print_structure()


if __name__ == "__main__":
    main()