import random


class Person:

    def __init__(self, name, age=0):
        self.name = name
        self.age = age


class Bus:

    def __init__(self, max_passengers=20):
        self.max_passengers = max_passengers
        self.passengers_list = []

    def add_passenger(self, passenger):
        if len(self.passengers_list) < self.max_passengers:

            self.passengers_list.append(passenger)
            print("A passenger boarded the bus")
        else:
            print("The bus is full. There is no space for more passengers")

    def remove_passenger(self):
        if len(self.passengers_list) != 0:
            self.passengers_list.pop(random.randrange(len(self.passengers_list)))
            print("A passenger got off the bus")
        else:
            print("The bus is empty")


def read_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Invalid input. You must enter an integer.")


def main():
    new_bus = Bus()

    option = 0

    while option != 3:
        option = read_int(f"""
Current number of passengers: {len(new_bus.passengers_list)}

1. Add a passenger
2. Remove a passenger
3. Exit

Enter an option: """)

        match option:

            case 1:
                new_passenger = Person(f"Passenger: {len(new_bus.passengers_list) + 1}",random.randint(10, 80))
                new_bus.add_passenger(new_passenger)

            case 2:
                new_bus.remove_passenger()

            case 3:
                input("Closing the program. Press Enter to finish.")

            case _:
                print("Invalid option")


if __name__ == "__main__":
    main()