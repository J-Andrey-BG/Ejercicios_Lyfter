import random

my_list = []
counter = 0

for index in range(20):
    random_number = random.randint(1,100)
    my_list.append(random_number)

print(my_list)

while counter < len(my_list):
    if my_list[counter] % 2 != 0:
        my_list.pop(counter)
        counter -= 1
    counter += 1

print(my_list)