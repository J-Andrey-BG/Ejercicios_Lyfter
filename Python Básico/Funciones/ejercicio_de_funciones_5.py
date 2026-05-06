my_string = "This Is A Sample String"


def up_down_case_count(string):
    lower_case_counter = 0
    upper_case_counter = 0
    for index in range(len(string)):
        if string[index].islower():
            lower_case_counter += 1
        elif string[index].isupper():
            upper_case_counter += 1
    print(f"There's {upper_case_counter} upper cases and {lower_case_counter} lower cases") 


up_down_case_count(my_string)