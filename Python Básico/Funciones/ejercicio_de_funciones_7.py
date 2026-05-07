import random


def create_prime_number_list(number_list):
    prime_number_list=[]
    for index in range(len(number_list)):
        if find_if_prime(number_list[index]):
            prime_number_list.append(number_list[index])
    return prime_number_list 


def find_if_prime(number):
    is_prime = True
    if number <= 0:
        is_prime = False
    else:
        for divider in range(2, number):
            if number % divider == 0:
                is_prime = False
                break
    return is_prime 


def create_list():
    my_list = []
    for index in range(random.randint(5,10)):
        random_number = random.randint(1,100)
        my_list.append(random_number)
    print(f"La lista es: {my_list}")
    return my_list


print(f"La lista de numeros primos es: {create_prime_number_list(create_list())}")