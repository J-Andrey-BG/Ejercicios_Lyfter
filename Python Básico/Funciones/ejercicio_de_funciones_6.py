my_string = "python-variable-funcion-computadora-monitor"


def sort_string(string):
    my_list = string.split("-")
    sorted_list = sorted(my_list, key=str.lower)
    sorted_string = "-".join(sorted_list)
    return sorted_string


print(sort_string(my_string))