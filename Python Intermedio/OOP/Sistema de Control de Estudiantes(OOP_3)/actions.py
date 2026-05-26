import re
import os
import entities


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
        same_name = student.name.strip().casefold() == name.strip().casefold()
        same_section = student.section.strip().upper() == section.strip().upper()

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
        print(f"Name: {student.name}")
        print(f"Section: {student.section}")
        print(f"Spanish grade: {student.spanish_grade}")
        print(f"English grade: {student.english_grade}")
        print(f"Social Studies grade: {student.social_studies_grade}")
        print(f"Science grade: {student.science_grade}")


def show_top_3_students(students_list):
    for student in students_list:
        student_average = student.create_average_grade_dict()

        print("")
        print(f"Name: {student_average['Name']}")
        print(f"Section: {student_average['Section']}")
        print(f"Average grade: {student_average['Average grade']:.2f}")


def show_failed_students(students_list):
    if not students_list:
        print("There are no failed students.")
        return

    for student in students_list:
        failed_grades = student.create_failed_grades_dict()

        print("")
        print(f"Name: {failed_grades['Name']}")
        print(f"Section: {failed_grades['Section']}")

        for key, value in failed_grades.items():
            if key != "Name" and key != "Section":
                print(f"{key}: {value}")


# ============================
# Student Management Functions
# ============================


def create_student_obj(students_list):
    while True:
        name = read_valid_name("Enter the student's full name: ")
        section = read_valid_section("Enter the student's section: ")

        if not student_exists(students_list, name, section):
            break

        print("A student with the same name and section already exists.")

    spanish_grade = read_int("Enter Spanish grade: ", 0, 100)
    english_grade = read_int("Enter English grade: ", 0, 100)
    social_studies_grade = read_int("Enter Social Studies grade: ", 0, 100)
    science_grade = read_int("Enter Science grade: ", 0, 100)

    student = entities.Student(
        name,
        section,
        spanish_grade,
        english_grade,
        social_studies_grade,
        science_grade
    )

    return student


def find_student(students_list):
    name = read_required_text("Enter the name of the student: ")
    section = read_valid_section("Enter the section of the student: ")

    for student in students_list:
        same_name = student.name.strip().casefold() == name.strip().casefold()
        same_section = student.section.strip().upper() == section.strip().upper()

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


def get_average_grade(grades_list):
    if len(grades_list) == 0:
        return 0

    average_grade = sum(grades_list) / len(grades_list)

    return average_grade


def get_students_average_grade(students_list):
    average_grade_list = []

    for student in students_list:
        grades_list = student.create_grades_list()
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
        if student.has_failed_grades():
            failed_students_list.append(student)

    return failed_students_list


def get_top_3_best_students(grades_list, students_list):
    sorted_index_list = get_sorted_index(grades_list)
    top_3_students = []

    top_3_index = sorted_index_list[-3:]

    for index in reversed(top_3_index):
        top_3_students.append(students_list[index])

    return top_3_students