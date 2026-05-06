import random

my_list = []

#primero crea una lista de un tamaño entre 5 y 10 con numeros del 1 al 10
# para cumplir que funcione con listas de cualquier tamaño
for index in range(random.randint(5,10)):
    random_number = random.randint(1,10)
    my_list.append(random_number)

print(my_list)

#Luego intercambia el primer numero de la lista con el ultimo
changing_number1 = my_list.pop(0)
changing_number2 = my_list.pop(len(my_list)-1)
my_list.append(changing_number1)
my_list.insert(0, changing_number2)

print(my_list)