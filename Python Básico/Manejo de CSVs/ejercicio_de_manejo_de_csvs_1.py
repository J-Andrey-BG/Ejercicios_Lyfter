import csv
from pathlib import Path


KEYS_LIST = ["Name", "Genre", "Developer", "Clasification ESRB"]
FILE_NAME = "games_list.csv"
VALID_ESRB_CLASSIFICATIONS = ["E", "E10+", "T", "M", "AO", "RP"]


def main():
    if Path(FILE_NAME).is_file():
        games_list = read_csv_file(FILE_NAME)
    else:
        games_list = []

    user_number = 0

    while user_number != 4:
        print("""---Main Menu---
1. Add New Game
2. Show list of games
3. Save CSV file
4. Exit
""")

        user_number = read_int("Enter an option: ")
        clear_terminal()

        match user_number:
            case 1:
                print("Adding new game...\n")
                add_game(games_list)
                clear_terminal()

            case 2:
                print(games_list)
                input("Press enter to continue")
                clear_terminal()

            case 3:
                save_csv_file(FILE_NAME, games_list)
                input("Press enter to continue")
                clear_terminal()

            case 4:
                print("Closing the program...")
                input("Press enter to finish")
                clear_terminal()

            case _:
                print("Invalid option.")
                input("Press enter to continue")
                clear_terminal()


def save_csv_file(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=KEYS_LIST)

            writer.writeheader()

            writer.writerows(data)

        print("CSV file saved successfully.")

    except PermissionError:
        print(f"You do not have permission to write the file {file_path}.")

    except csv.Error:
        print("There was an error writing the CSV file.")

    except Exception as ex:
        print(f"Unexpected error while saving the file: {ex}")


def read_csv_file(file_path):
    games_list = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for game in reader:
                games_list.append(game)

    except FileNotFoundError:
        print(f"The file {file_path} was not found.")

    except PermissionError:
        print(f"You do not have permission to read the file {file_path}.")

    except csv.Error:
        print("There was an error reading the CSV file.")

    except Exception as ex:
        print(f"Unexpected error while reading the file: {ex}")

    return games_list


def add_game (games_list):
    games_list.append(create_dictionary())


def create_dictionary():
    games_dictionary = {}

    for keys in KEYS_LIST:
        games_dictionary[keys] = enter_information(keys)

    return games_dictionary


def enter_information(column):
    match column:
        case "Name":
            return enter_required_text(column)

        case "Genre":
            return enter_required_text(column)

        case "Developer":
            return enter_required_text(column)

        case "Clasification ESRB":
            return enter_esrb_classification()

        case _:
            return enter_required_text(column)


def enter_esrb_classification():
    while True:
        print("Valid ESRB classifications:")
        print("E, E10+, T, M, AO, RP")

        classification = input("Enter the Clasification ESRB: ").strip().upper()

        if classification in VALID_ESRB_CLASSIFICATIONS:
            return classification

        print("Invalid ESRB classification. Please enter a valid option.")


def enter_required_text(column):
    while True:
        data = input(f"Enter the {column}: ").strip()

        if data != "":
            return data

        print(f"The {column} cannot be empty.")


def read_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Invalid input. You must enter an integer.")


def clear_terminal():
    print("\033[H\033[J", end="")


main()