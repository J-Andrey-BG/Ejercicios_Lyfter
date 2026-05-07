print("""---- Encontrar el número mayor ----

Ingrese 3 números """)

user_numbers = [0, 0, 0]

for index in range(3):
    user_numbers[index] = int(input())

greater_number = user_numbers[0]

for index in range(1, 3):
    if greater_number < user_numbers [index]:
        greater_number = user_numbers [index]


print(f"El numero mayor de los 3 ingresados es: {greater_number}")

