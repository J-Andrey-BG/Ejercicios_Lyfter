from datetime import date


class User:
    def __init__(self, date_of_birth):
        self.date_of_birth = date_of_birth

    @property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year

        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1

        return age


def validate_adult_user(func):
    def wrapper(user, *args, **kwargs):
        if not isinstance(user, User):
            raise TypeError("The parameter must be a User.")

        if user.age < 18:
            raise ValueError("The user must be over 18 years old.")

        return func(user, *args, **kwargs)

    return wrapper


@validate_adult_user
def enter_site(user):
    return "Access granted."


adult_user = User(date(2000, 5, 10))
minor_user = User(date(2010, 3, 20))

try:
    print(enter_site(adult_user))
except Exception as ex:
    print(f"Error: {ex}")

try:
    print(enter_site(minor_user))
except Exception as ex:
    print(f"Error: {ex}")