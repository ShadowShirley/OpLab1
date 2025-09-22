from modelPerson import Person

class PersonValidator:
    @staticmethod
    def validate(person: Person) -> list[str]:
        errors = []
        if not person.last_name.strip():
            errors.append("❌ Фамилия обязательна")
        if not person.first_name.strip():
            errors.append("❌ Имя обязательно")
        if person.work_from < person.birth_date:
            errors.append("❌ Дата начала работы не может быть раньше даты рождения")
        return errors