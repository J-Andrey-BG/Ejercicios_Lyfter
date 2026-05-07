list_a = ["first_name", "last_name", "role", "language", "age", "city"]
list_b = ["Jerry", "Brenes", "Student", "spanish", 24, "Cartago"]

new_dictionary = {}

for index in range(len(list_a)):
    new_dictionary[list_a[index]] = list_b[index] 

print(new_dictionary)