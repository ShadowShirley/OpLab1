from modelPerson import Person

class PensionService:
    @staticmethod
    def generate_report(person: Person) -> str:
        age = person.calculate_age()
        exp = person.calculate_experience()
        pension_age = 60 if person.gender == "М" else 55
        req_exp = person.required_experience()

        report = f"ОСНОВНАЯ ИНФОРМАЦИЯ\n"
        report += f"Возраст: {age} лет\n"
        report += f"Стаж: {exp} лет\n\n"
        report += f"ПЕНСИОННАЯ ИНФОРМАЦИЯ\n"
        report += f"Пенсионный возраст: {pension_age} лет\n"
        report += f"На пенсии: {'Да' if person.is_retired() else 'Нет'}\n"
        report += f"До пенсии: {person.years_until_retirement()}\n\n"
        report += f"СТАЖ\n"
        report += f"Минимальный стаж: {req_exp} лет\n"
        report += f"Статус стажа: {person.experience_status()}\n"

        if person.is_retired() and person.has_enough_experience():
            report += "\nСотрудник имеет право на пенсию"
        elif person.is_retired():
            report += "\nДостигнут пенсионный возраст, но стаж недостаточный"
        elif person.has_enough_experience():
            report += "\nСтаж достаточный, но пенсионный возраст еще не наступил"

        return report