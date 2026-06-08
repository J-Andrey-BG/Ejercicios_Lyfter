import math


class Circle:

    def __init__(self, radius):
        self.radius = radius


    def get_area(self):
        pi_number = math.pi

        circule_area = pi_number * (self.radius ** 2)

        return circule_area