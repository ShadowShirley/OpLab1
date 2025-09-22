import csv
from pathlib import Path
from typing import List
from modelPerson import Person
from datetime import datetime

class PersonRepository:
    def __init__(self, filename: str = "persons.csv"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        Path(self.filename).touch(exist_ok=True)

    def load_all(self) -> List[Person]:
        persons = []
        try:
            with open(self.filename, newline="", encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 7:
                        continue
                    try:
                        person = Person(
                            id=int(row[0]),
                            last_name=row[1],
                            first_name=row[2],
                            middle_name=row[3],
                            gender=row[4],
                            birth_date=datetime.strptime(row[5], '%d.%m.%Y').date(),
                            work_from=datetime.strptime(row[6], '%d.%m.%Y').date()
                        )
                        persons.append(person)
                    except (ValueError, IndexError):
                        continue  # Пропускаем битые строки
        except FileNotFoundError:
            pass
        except Exception as e:
            raise RuntimeError(f"Ошибка загрузки данных: {e}")
        return persons

    def save_all(self, persons: List[Person]):
        try:
            with open(self.filename, "w", newline="", encoding='utf-8') as f:
                writer = csv.writer(f)
                for p in persons:
                    writer.writerow([
                        p.id,
                        p.last_name,
                        p.first_name,
                        p.middle_name,
                        p.gender,
                        p.birth_date.strftime('%d.%m.%Y'),
                        p.work_from.strftime('%d.%m.%Y')
                    ])
        except Exception as e:
            raise RuntimeError(f"Ошибка сохранения данных: {e}")