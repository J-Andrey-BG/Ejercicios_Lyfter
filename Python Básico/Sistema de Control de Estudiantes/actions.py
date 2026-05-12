import re
import os


# ==============
# Read Functions
# ==============


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


def read_required_text(message):
    while True:
        data = input(message).strip()

        if data != "":
            return data

        print("This field cannot be empty.")


def read_boolean(message):
    while True:
        answer = input(message).strip().lower()

        if answer == "yes":
            return True

        if answer == "no":
            return False

        print("Invalid input. You must enter yes or no.")


# ====================
# Validation Functions
# ====================


def student_exists(students_list, name, section):
    for student in students_list:
        same_name = student["Name"].strip().casefold() == name.strip().casefold()
        same_section = student["Section"].strip().upper() == section.strip().upper()

        if same_name and same_section:
            return True

    return False


def read_valid_name(message):
    while True:
        name = input(message).strip()

        if is_valid_name(name):
            return name

        print("Invalid name. The name cannot be empty or contain numbers.")


def is_valid_name(name):
    if name.strip() == "":
        return False

    for character in name:
        if character.isdigit():
            return False

    return True


def read_valid_section(message):
    while True:
        section = read_required_text(message).upper()

        if verify_section_format(section):
            return section

        print("Invalid section format. Example: 10A, 11B, 12C.")


def verify_section_format(section):
    pattern = r"^[0-9]{2}[A-Z]$"

    return re.match(pattern, section) is not None


# ===================
# Interface Functions
# ===================


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def show_all_students(students_list):
    for student in students_list:
        print("")

        for key, value in student.items():
            print(f"{key}: {value}")


# ============================
# Student Management Functions
# ============================


def create_student_dict(students_list):
    student = {}

    while True:
        name = read_valid_name("Enter the student's full name: ")
        section = read_valid_section("Enter the student's section: ")

        if not student_exists(students_list, name, section):
            break

        print("A student with the same name and section already exists.")

    student["Name"] = name
    student["Section"] = section
    student["Spanish grade"] = read_int("Enter Spanish grade: ", 0, 100)
    student["English grade"] = read_int("Enter English grade: ", 0, 100)
    student["Social Studies grade"] = read_int("Enter Social Studies grade: ", 0, 100)
    student["Science grade"] = read_int("Enter Science grade: ", 0, 100)

    return student


def find_student(students_list):
    name = read_required_text("Enter the name of the student: ")
    section = read_valid_section("Enter the section of the student: ")

    for student in students_list:
        same_name = student["Name"].strip().casefold() == name.strip().casefold()
        same_section = student["Section"].strip().upper() == section.strip().upper()

        if same_name and same_section:
            print("Student found")
            input("\nPress Enter to continue")
            return student

    print("Student not found")
    input("\nPress Enter to continue")
    return None


def remove_student(student_to_remove, student_list):
    for student in student_list:
        if student == student_to_remove:
            student_list.remove(student)
            break

    return student_list


# ===========================
# Grade Calculation Functions
# ===========================


def get_grades_list(student):
    grades_list = []
    for value in student.values():
        if isinstance(value, int):
            grades_list.append(value)

    return grades_list


def get_average_grade(grades_list):
    if len(grades_list) == 0:
        return 0

    average_grade = sum(grades_list) / len(grades_list)

    return average_grade


def get_students_average_grade(students_list):
    average_grade_list = []

    for student in students_list:
        grades_list = get_grades_list(student)
        average_grade_list.append(get_average_grade(grades_list))

    return average_grade_list


# =================
# Sorting Functions
# =================


def get_sorted_index(grades_list):
    index_list = list(range(len(grades_list)))

    for index_i in range(len(grades_list)):
        min_index = index_i

        for index_j in range(index_i + 1, len(grades_list)):
            if grades_list[index_j] < grades_list[min_index]:
                min_index = index_j

        grades_list[index_i], grades_list[min_index] = grades_list[min_index], grades_list[index_i]
        index_list[index_i], index_list[min_index] = index_list[min_index], index_list[index_i]

    return index_list


# =================
# Report Functions
# =================


def get_failed_students(students_list):
    failed_students_list = []

    for student in students_list:
        for value in student.values():
            if isinstance(value, int) and value < 60:
                failed_students_list.append(student)  
                break

    return failed_students_list


def create_failed_students_dict(students_list):
    failed_students_list = []

    try:
        for student in students_list:
            failed_student = {
                "Name": student["Name"],
                "Section": student["Section"]
            }

            has_failed_subject = False

            for key, value in student.items():
                if isinstance(value, int) and value < 60:
                    failed_student[key] = value
                    has_failed_subject = True

            if has_failed_subject:
                failed_students_list.append(failed_student)

    except KeyError:
        print("There is a student record with missing Name or Section.")

    return failed_students_list


def convert_grades_to_average(students_list):
    students_list_with_average = []

    for student in students_list:
        grades_list = get_grades_list(student)
        average_grade = get_average_grade(grades_list)

        new_student = {}

        for key, value in student.items():
            if not isinstance(value, int):
                new_student[key] = value

        new_student["Average grade"] = average_grade

        students_list_with_average.append(new_student)

    return students_list_with_average


def get_top_3_best_students(grades_list, students_list):
    sorted_index_list = get_sorted_index(grades_list)
    top_3_students = []

    top_3_index = sorted_index_list[-3:]

    for index in reversed(top_3_index):
        top_3_students.append(students_list[index].copy())

    top_3_students = convert_grades_to_average(top_3_students)

    return top_3_students