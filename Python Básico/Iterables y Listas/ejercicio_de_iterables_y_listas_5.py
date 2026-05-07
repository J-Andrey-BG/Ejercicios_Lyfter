print("---- Crea una lista de 10 números ----")

user_list = []

for index in range(10):
    user_list.insert(index, int(input(f"Ingrese el numero {index + 1} ")))

greater_number = user_list[0]

for index in range(1, 10):
    if greater_number < user_list [index]:
        greater_number = user_list [index]

print(f"{user_list} El más alto fue {greater_number}. ")