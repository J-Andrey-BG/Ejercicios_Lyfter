import csv


def save_csv_file(data, file_path="students.csv"):
    KEYS_LIST = ["Name","Section","Spanish grade","English grade","Social Studies grade","Science grade"]
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


def read_csv_file(students_list, file_path="students.csv"):

    grade_keys = [
        "Spanish grade",
        "English grade",
        "Social Studies grade",
        "Science grade"
    ]

    imported_students = 0
    skipped_students = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for student in reader:
                name = student["Name"].strip()
                section = student["Section"].strip().upper()

                if student_exists(students_list, name, section):
                    skipped_students += 1
                    continue

                student["Name"] = name
                student["Section"] = section

                for key in grade_keys:
                    student[key] = int(student[key])

                students_list.append(student)
                imported_students += 1

        print("CSV file loaded successfully.")
        print(f"Imported students: {imported_students}")
        print(f"Skipped duplicated students: {skipped_students}")

    except FileNotFoundError:
        print(f"The file {file_path} was not found.")

    except PermissionError:
        print(f"You do not have permission to read the file {file_path}.")

    except csv.Error:
        print("There was an error reading the CSV file.")

    except ValueError:
        print("The CSV file contains an invalid grade.")

    except KeyError:
        print("The CSV file does not have the required columns.")

    except Exception as ex:
        print(f"Unexpected error while reading the file: {ex}")

    return students_list


def student_exists(students_list, name, section):
    for student in students_list:
        same_name = student["Name"].strip().casefold() == name.strip().casefold()
        same_section = student["Section"].strip().upper() == section.strip().upper()

        if same_name and same_section:
            return True

    return False