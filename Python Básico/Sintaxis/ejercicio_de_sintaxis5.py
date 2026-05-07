grade_counter = 1
approved_grades_quantity = 0
failed_grades_quantity = 0
approved_grades_average = 0
failed_grades_average = 0
total_grades_average = 0

print("---- Calculadora de promedios ----")
total_grades = int(input("Ingrese la cantidad de notas "))

while grade_counter <= total_grades:
    current_grade = int(input(f"Ingrese la nota numero: {grade_counter} "))
    if current_grade < 70:
        failed_grades_quantity += 1
        failed_grades_average += current_grade
    else:
        approved_grades_quantity += 1
        approved_grades_average += current_grade
    total_grades_average += (current_grade / total_grades)
    grade_counter += 1

if failed_grades_quantity != 0:
    failed_grades_average /= failed_grades_quantity
if approved_grades_quantity != 0:
    approved_grades_average /= approved_grades_quantity


print(f"""
El estudiante tiene esta cantidad de notas aprobadas: {approved_grades_quantity}

Este es el promedio de notas aprobadas: {approved_grades_average}

El estudiante tiene esta cantidad de notas desaprobadas: {failed_grades_quantity}

Este es el promedio de notas desaprobadas: {failed_grades_average}

Este es el promedio total de notas: {total_grades_average}""")