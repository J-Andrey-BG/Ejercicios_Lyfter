class Category:
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"])


class Movement:
    def __init__(self, title, amount, category, movement_type):
        self.title = title
        self.amount = amount
        self.category = category
        self.movement_type = movement_type

    def to_dict(self):
        return {
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "movement_type": self.movement_type,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["amount"],
            data["category"],
            data["movement_type"],
        )