import actions
import data


def menu_controls():

    user_choice = 0
    students_list = []

    while user_choice != 9:
        actions.clear_terminal()
        print_menu_in_terminal()
        user_choice = actions.read_int("\nSelect one option: ")
        actions.clear_terminal()

        match user_choice:

            case 1:
                print("Adding new student...\n")

                new_student = actions.create_student_dict(students_list)
                students_list.append(new_student)

                actions.clear_terminal()
                print("Student added successfully.\n")
                input("\nPress Enter to continue")

            case 2:
                print("Removing student...\n")

                requested_student = actions.find_student(students_list)

                if requested_student is not None:
                    answer = actions.read_boolean(
                        f"The student -{requested_student['Name']}- will be removed. "
                        "Are you sure you want to continue? yes/no "
                    )

                    if answer:
                        students_list = actions.remove_student(requested_student, students_list)
                        print("Student removed successfully.\n")
                        input("\nPress Enter to continue")

                    else:
                        print("Operation cancelled.\n")
                        input("\nPress Enter to continue")

                else:
                    print("Student was not found.\n")
                    input("\nPress Enter to continue")

            case 3:
                if not students_list:
                    print("No students have been added.\nAdd new students or import a CSV file.")
                    input("\nPress Enter to continue")
                    actions.clear_terminal()

                else:
                    print("Showing all students...")
                    actions.show_all_students(students_list)
                    input("\nPress Enter to continue")
                    actions.clear_terminal()

            case 4:
                print("Showing top 3 students...")

                all_average_grades = actions.get_students_average_grade(students_list)
                top_3_students = actions.get_top_3_best_students(all_average_grades, students_list)

                actions.show_all_students(top_3_students)
                input("\nPress Enter to continue")
                actions.clear_terminal()

            case 5:
                print("Showing all failed students...")

                failed_students = actions.get_failed_students(students_list)
                failed_students_dict = actions.create_failed_students_dict(failed_students)

                actions.show_all_students(failed_students_dict)
                input("\nPress Enter to continue")

            case 6:
                print("Showing the average grade of all students...\n")

                average_grades_list = actions.get_students_average_grade(students_list)
                general_average_grade = actions.get_average_grade(average_grades_list)

                print(f"The average grade of all students is: {general_average_grade:.2f}")
                input("\nPress Enter to continue")

            case 7:
                actions.clear_terminal()

                students_list = data.read_csv_file(students_list)

                input("\nPress Enter to continue")

            case 8:
                actions.clear_terminal()

                data.save_csv_file(students_list)

                input("\nPress Enter to continue")

            case 9:
                print("Exiting the program...")
                input("Press Enter to finish")
                actions.clear_terminal()

            case _:
                print("Invalid option. Please select a valid menu option.")
                input("\nPress Enter to continue")


def print_menu_in_terminal():
    print("======Welcome to the Student Management System======\n")
    print("""                   Main Menu

1. Add student

2. Remove student

3. View all students

4. Top 3 students

5. Show failed students

6. Average grade of all students

7. Import data from CSV

8. Export data to CSV

9. Exit""")