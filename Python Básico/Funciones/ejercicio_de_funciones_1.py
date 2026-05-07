import random


def create_random_number():
    number = random.randint(1,10)
    print(f"numero aleatorio: {number}" )
    counter(number)


def counter(number):
    for index in range(number):
        print(f"Esta función cuenta hasta llegar al numero aleatorio: {index+1}")


create_random_number()