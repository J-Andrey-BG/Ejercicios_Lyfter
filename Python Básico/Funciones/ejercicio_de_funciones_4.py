my_string = "Hola Mundo"


def turn_around_function(string):
    my_turned_string = ""
    for index in range(len(string)-1, -1, -1):
        my_turned_string += string[index]
    return my_turned_string


print(my_string)
print(turn_around_function(my_string))