import random


def sum_of_elements(my_list):
    total_sum = 0
    for index in range(len(my_list)):
        total_sum += my_list[index]
    return total_sum


def create_list():
    my_list = []
    for index in range(random.randint(5,10)):
        random_number = random.randint(1,10)
        my_list.append(random_number)
    print(f"La lista es: {my_list}")
    return my_list


sum_of_all_elements = sum_of_elements(create_list())
print(f"El resultado de la suma de todos los elementos de la lista es: {sum_of_all_elements}")