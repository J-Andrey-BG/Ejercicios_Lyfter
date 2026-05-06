list_of_keys = ["access_level", "age"]
list_counter = 0

employee = {
    "name":" John",
    "email": "john@ecorp.com",
    "access_level": 5,
    "age": 28
    }

# usé employee.copy para iterar una copia del diccionario
# y que no genere un RuntimeError: dictionary changed size during iteration
# al eliminar un elemento
for keys in employee.copy():
    for index in range(len(list_of_keys)):
        if keys == list_of_keys[index]:
            employee.pop(list_of_keys[index])

print(employee)