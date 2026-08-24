from datetime import date


def get_today_string():
    return date.today().strftime("%d/%m/%Y")


class Category:
    def __init__(self, name, color="#FFFFFF"):
        self.name = name
        self.color = color

    def to_dict(self):
        return {
            "name": self.name,
            "color": self.color,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data.get("color", "#FFFFFF"),
        )


class Movement:
    def __init__(
        self,
        title,
        amount,
        category,
        movement_type,
        movement_date=None,
    ):
        self.title = title
        self.amount = amount
        self.category = category
        self.movement_type = movement_type
        self.date = movement_date if movement_date is not None else get_today_string()

    def to_dict(self):
        return {
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "movement_type": self.movement_type,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["amount"],
            data["category"],
            data["movement_type"],
            data.get("date", get_today_string()),
        )