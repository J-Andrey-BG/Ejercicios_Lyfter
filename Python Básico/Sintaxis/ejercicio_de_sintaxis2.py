print("---- Clasificador de Etapa de Vida ----")

name = input("Ingrese su nombre: ")
last_name = input("Ingrese su apellido: ")
age = int(input("Ingrese su edad: "))
life_stage = ""

if age < 4:
    life_stage = "bebé"
elif age < 11:
    life_stage = "niño"
elif age < 13:
    life_stage = "preadolescente"
elif age < 19:
    life_stage = "adolescente"
elif age < 41:
    life_stage = "adulto joven"
elif age < 66:
    life_stage = "adulto"
else:
    life_stage = "adulto mayor"

print(f"""Hola! {name} {last_name}
La etapa de la vida en la que te encuentras es: {life_stage}""")