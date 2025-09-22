from dataclasses import dataclass
from datetime import date

@dataclass
class Person:
    id: int
    last_name: str
    first_name: str
    middle_name: str
    gender: str  # "М" или "Ж"
    birth_date: date
    work_from: date

    def calculate_age(self, on_date=None) -> int:
        if on_date is None:
            on_date = date.today()
        return on_date.year - self.birth_date.year - (
            (on_date.month, on_date.day) < (self.birth_date.month, self.birth_date.day)
        )

    def calculate_experience(self, on_date=None) -> int:
        if on_date is None:
            on_date = date.today()
        return on_date.year - self.work_from.year - (
            (on_date.month, on_date.day) < (self.work_from.month, self.work_from.day)
        )

    def is_retired(self) -> bool:
        pension_age = 60 if self.gender == "М" else 55
        return self.calculate_age() >= pension_age

    def required_experience(self) -> int:
        return 25 if self.gender == "М" else 20

    def has_enough_experience(self) -> bool:
        return self.calculate_experience() >= self.required_experience()

    def years_until_retirement(self) -> int | str:
        if self.is_retired():
            return "Уже на пенсии"
        pension_age = 60 if self.gender == "М" else 55
        return pension_age - self.calculate_age()

    def experience_status(self) -> str:
        req = self.required_experience()
        exp = self.calculate_experience()
        if exp >= req:
            return "Достаточный"
        else:
            return f"Недостаточный (еще {req - exp} лет)"

    def get_short_name(self) -> str:
        parts = [self.last_name]
        if self.first_name:
            parts.append(f"{self.first_name[0]}.")
        if self.middle_name:
            parts.append(f"{self.middle_name[0]}.")
        return " ".join(parts)