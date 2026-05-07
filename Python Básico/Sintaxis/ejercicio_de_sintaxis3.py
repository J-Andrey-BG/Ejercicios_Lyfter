import random

print("---- Adivina el numero aleatorio ----")
print("")

secret_number = random.randint(1, 10)

user_number = int(input("Elige un numero del 1 al 10: "))

while user_number != secret_number:
    print("Número incorrecto!!")
    user_number = int(input("Elige otro numero del 1 al 10: "))

print("Correcto!!")
print(f"El número era: {secret_number}")