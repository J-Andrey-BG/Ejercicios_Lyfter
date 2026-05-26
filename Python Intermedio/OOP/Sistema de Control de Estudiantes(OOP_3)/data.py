import csv
import entities


def save_csv_file(students_list, file_path="students.csv"):
    keys_list = [
        "Name",
        "Section",
        "Spanish grade",
        "English grade",
        "Social Studies grade",
        "Science grade"
    ]

    students_dict_list = []

    for student in students_list:
        students_dict_list.append(student.to_dict())

    try:
        with open(file_path, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=keys_list)

            writer.writeheader()
            writer.writerows(students_dict_list)

        print("CSV file saved successfully.")

    except PermissionError:
        print(f"You do not have permission to write the file {file_path}.")

    except csv.Error:
        print("There was an error writing the CSV file.")

    except Exception as ex:
        print(f"Unexpected error while saving the file: {ex}")


def read_csv_file(students_list, file_path="students.csv"):
    imported_students = 0
    skipped_students = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for student_data in reader:
                name = student_data["Name"].strip()
                section = student_data["Section"].strip().upper()

                if student_exists(students_list, name, section):
                    skipped_students += 1
                    continue

                spanish_grade = int(student_data["Spanish grade"])
                english_grade = int(student_data["English grade"])
                social_studies_grade = int(student_data["Social Studies grade"])
                science_grade = int(student_data["Science grade"])

                student = entities.Student(
                    name,
                    section,
                    spanish_grade,
                    english_grade,
                    social_studies_grade,
                    science_grade
                )

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
        same_name = student.name.strip().casefold() == name.strip().casefold()
        same_section = student.section.strip().upper() == section.strip().upper()

        if same_name and same_section:
            return True

    return False