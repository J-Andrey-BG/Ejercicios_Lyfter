class Student:

    def __init__(self, name, section, spanish_grade, english_grade, social_studies_grade, science_grade):
        self.name = name
        self.section = section
        self.spanish_grade = spanish_grade
        self.english_grade = english_grade
        self.social_studies_grade = social_studies_grade
        self.science_grade = science_grade

    def create_grades_list(self):
        grades_list = []

        grades_list.append(self.spanish_grade)
        grades_list.append(self.english_grade)
        grades_list.append(self.social_studies_grade)
        grades_list.append(self.science_grade)

        return grades_list

    def get_average_grade(self):
        grades_list = self.create_grades_list()

        if len(grades_list) == 0:
            return 0

        average_grade = sum(grades_list) / len(grades_list)

        return average_grade

    def has_failed_grades(self):
        if self.spanish_grade < 60:
            return True

        if self.english_grade < 60:
            return True

        if self.social_studies_grade < 60:
            return True

        if self.science_grade < 60:
            return True

        return False

    def create_failed_grades_dict(self):
        failed_grades = {}

        failed_grades["Name"] = self.name
        failed_grades["Section"] = self.section

        if self.spanish_grade < 60:
            failed_grades["Spanish grade"] = self.spanish_grade

        if self.english_grade < 60:
            failed_grades["English grade"] = self.english_grade

        if self.social_studies_grade < 60:
            failed_grades["Social Studies grade"] = self.social_studies_grade

        if self.science_grade < 60:
            failed_grades["Science grade"] = self.science_grade

        return failed_grades

    def create_average_grade_dict(self):
        student_average = {}

        student_average["Name"] = self.name
        student_average["Section"] = self.section
        student_average["Average grade"] = self.get_average_grade()

        return student_average

    def to_dict(self):
        student_dict = {}

        student_dict["Name"] = self.name
        student_dict["Section"] = self.section
        student_dict["Spanish grade"] = self.spanish_grade
        student_dict["English grade"] = self.english_grade
        student_dict["Social Studies grade"] = self.social_studies_grade
        student_dict["Science grade"] = self.science_grade

        return student_dict