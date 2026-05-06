import json
from pathlib import Path

FILE_NAME = "pokemon.json"


def main():
    pokemon_list = read_json_file(FILE_NAME)

    new_pokemon = create_pokemon()
    pokemon_list.append(new_pokemon)

    save_json_file(FILE_NAME, pokemon_list)

    print("Pokémon added successfully.")


def read_json_file(file_path):
    if not Path(file_path).is_file():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("Error: The JSON file has an invalid format.")
        return []

    except PermissionError:
        print("Error: You do not have permission to read the file.")
        return []

    except Exception as ex:
        print(f"Unexpected error while reading the file: {ex}")
        return []


def save_json_file(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except PermissionError:
        print("Error: You do not have permission to write the file.")

    except Exception as ex:
        print(f"Unexpected error while saving the file: {ex}")


def create_pokemon():
    pokemon = {}

    pokemon["name"] = read_required_text("Enter the Pokémon name: ")
    pokemon["type"] = read_required_text("Enter the Pokémon type: ")
    pokemon["level"] = read_int("Enter the Pokémon level: ", 1, 100)
    pokemon["weight_kg"] = read_float("Enter the Pokémon weight in kg: ", 0.1)
    pokemon["is_shiny"] = read_boolean("Is the Pokémon shiny? yes/no: ")
    pokemon["held_item"] = read_optional_text("Enter held item, or leave empty if none: ")
    pokemon["skills"] = read_skills()
    pokemon["stats"] = read_stats()

    return pokemon


def read_required_text(message):
    while True:
        data = input(message).strip()

        if data != "":
            return data

        print("This field cannot be empty.")


def read_optional_text(message):
    data = input(message).strip()

    if data == "":
        return None

    return data


def read_int(message, min_value=None, max_value=None):
    while True:
        try:
            number = int(input(message))

            if min_value is not None and number < min_value:
                print(f"The number must be greater than or equal to {min_value}.")
                continue

            if max_value is not None and number > max_value:
                print(f"The number must be less than or equal to {max_value}.")
                continue

            return number

        except ValueError:
            print("Invalid input. You must enter an integer.")


def read_float(message, min_value=None, max_value=None):
    while True:
        try:
            number = float(input(message))

            if min_value is not None and number < min_value:
                print(f"The number must be greater than or equal to {min_value}.")
                continue

            if max_value is not None and number > max_value:
                print(f"The number must be less than or equal to {max_value}.")
                continue

            return number

        except ValueError:
            print("Invalid input. You must enter a decimal number.")


def read_boolean(message):
    while True:
        answer = input(message).strip().lower()

        if answer == "yes":
            return True

        if answer == "no":
            return False

        print("Invalid input. You must enter yes or no.")


def read_skills():
    skills = []

    for index in range(4):
        skill = read_required_text(f"Enter skill #{index + 1}: ")
        skills.append(skill)

    return skills


def read_stats():
    stats = {}

    stats["hp"] = read_int("Enter HP: ", 1)
    stats["attack"] = read_int("Enter attack: ", 1)
    stats["defense"] = read_int("Enter defense: ", 1)
    stats["sp_attack"] = read_int("Enter special attack: ", 1)
    stats["sp_defense"] = read_int("Enter special defense: ", 1)
    stats["speed"] = read_int("Enter speed: ", 1)

    return stats


main()