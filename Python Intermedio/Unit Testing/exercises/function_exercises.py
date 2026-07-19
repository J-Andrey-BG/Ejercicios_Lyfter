def sum_of_elements(number_list):
    total_sum = 0

    for index in range(len(number_list)):
        total_sum += number_list[index]

    return total_sum


def reverse_string(string):
    reversed_string = ""

    for index in range(len(string) - 1, -1, -1):
        reversed_string += string[index]

    return reversed_string


def count_upper_and_lower_cases(string):
    lower_case_counter = 0
    upper_case_counter = 0

    for index in range(len(string)):
        if string[index].islower():
            lower_case_counter += 1
        elif string[index].isupper():
            upper_case_counter += 1

    print(f"There's {upper_case_counter} upper cases and {lower_case_counter} lower cases")


def sort_hyphen_separated_words(string):
    word_list = string.split("-")
    sorted_list = sorted(word_list, key=str.lower)
    sorted_string = "-".join(sorted_list)

    return sorted_string


def create_prime_number_list(number_list):
    prime_number_list = []

    for index in range(len(number_list)):
        if find_if_prime(number_list[index]):
            prime_number_list.append(number_list[index])

    return prime_number_list


def find_if_prime(number):
    is_prime = True

    if number <= 1:
        is_prime = False
    else:
        for divider in range(2, number):
            if number % divider == 0:
                is_prime = False
                break

    return is_prime