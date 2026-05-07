user_number = 0
current_number = 0


def clear_terminal():
    print("\033[H\033[J", end="")


def read_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Invalid input. You must enter an integer.")


while user_number != 6:
    print("""---Main Menu---
1. Addition
2. Subtraction
3. Multiplication
4. Division
5. Clear results
6. Exit
""")

    user_number = read_int("Enter an option: ")
    clear_terminal()

    match user_number:
        case 1:
            print("-----Addition------")
            print(f"The current number is {current_number}")

            answer = read_int("Enter the number you want to add: ")
            current_number += answer

            print(f"The result of the operation is: {current_number}")
            input("Press enter to continue")
            clear_terminal()

        case 2:
            print("----Subtraction----")
            print(f"The current number is {current_number}")

            answer = read_int("Enter the number you want to subtract: ")
            current_number -= answer

            print(f"The result of the operation is: {current_number}")
            input("Press enter to continue")
            clear_terminal()

        case 3:
            print("---Multiplication---")
            print(f"The current number is {current_number}")

            answer = read_int("Enter the number you want to multiply by: ")
            current_number *= answer

            print(f"The result of the operation is: {current_number}")
            input("Press enter to continue")
            clear_terminal()

        case 4:
            print("-----Division-----")
            print(f"The current number is {current_number}")

            answer = read_int("Enter the number you want to divide by: ")

            while answer == 0:
                print("It is not possible to divide by 0.")
                answer = read_int("Enter a number different from 0: ")
            clear_terminal()

            current_number /= answer

            print(f"The result of the operation is: {current_number}")
            input("Press enter to continue")
            clear_terminal()

        case 5:
            current_number = 0

            print("Results cleared")
            print(f"The current number is {current_number}")
            input("Press enter to continue")
            clear_terminal()

        case 6:
            print("Closing the program...")
            input("Press enter to finish")
            clear_terminal()

        case _:
            print("Invalid option.")
            input("Press enter to continue")
            clear_terminal()