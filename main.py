import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from datetime import date
from tkcalendar import DateEntry

# Импортируем наши модули
from modelPerson import Person
from repository import PersonRepository
from services import PensionService
from validator import PersonValidator


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Настройка главного окна
        self.title("База данных сотрудников")
        self.geometry("1200x550")
        self.repo = PersonRepository()
        self.persons = self.repo.load_all()

        # Создание UI
        self.create_entries()
        self.create_buttons()
        self.create_treeview()
        self._refresh_treeview()

    def create_entries(self):
        self.entry_frame = ttk.Frame(self)
        self.entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Метки
        labels = ["Фамилия", "Имя", "Отчество", "Пол", "Дата рождения", "Работает с"]
        for i, text in enumerate(labels):
            ttk.Label(self.entry_frame, text=text).grid(row=0, column=i, padx=5, pady=5)

        # Поля ввода
        self.entry1 = ttk.Entry(self.entry_frame, width=15)
        self.entry2 = ttk.Entry(self.entry_frame, width=15)
        self.entry3 = ttk.Entry(self.entry_frame, width=15)

        self.gender_var = tk.StringVar()
        self.entry4 = ttk.Combobox(self.entry_frame, textvariable=self.gender_var,
                                   values=["М", "Ж"], width=13, state="readonly")
        self.entry4.set("М")

        self.entry5 = DateEntry(self.entry_frame, width=13, date_pattern='dd.mm.yyyy')
        self.entry6 = DateEntry(self.entry_frame, width=13, date_pattern='dd.mm.yyyy')

        # Размещение
        self.entry1.grid(row=1, column=0, padx=5, pady=5)
        self.entry2.grid(row=1, column=1, padx=5, pady=5)
        self.entry3.grid(row=1, column=2, padx=5, pady=5)
        self.entry4.grid(row=1, column=3, padx=5, pady=5)
        self.entry5.grid(row=1, column=4, padx=5, pady=5)
        self.entry6.grid(row=1, column=5, padx=5, pady=5)

    def create_buttons(self):
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.btn_add = ttk.Button(self.button_frame, text="Добавить", command=self.add_person)
        self.btn_edit = ttk.Button(self.button_frame, text="Изменить", command=self.edit_person)
        self.btn_delete = ttk.Button(self.button_frame, text="Удалить", command=self.delete_person)
        self.btn_clear = ttk.Button(self.button_frame, text="Очистить", command=self.clear_entries)

        self.btn_add.grid(row=0, column=0, padx=5, pady=5)
        self.btn_edit.grid(row=0, column=1, padx=5, pady=5)
        self.btn_delete.grid(row=0, column=2, padx=5, pady=5)
        self.btn_clear.grid(row=0, column=3, padx=5, pady=5)

    def create_treeview(self):
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        columns = ("ID", "Фамилия", "Имя", "Отчество", "Пол", "Дата рождения", "Работает с")
        self.tree = ttk.Treeview(self.tree_frame, show="headings", columns=columns, height=15)

        # Заголовки
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor="center")
            elif col in ("Пол", "Дата рождения", "Работает с"):
                self.tree.column(col, width=100, anchor="center")
            else:
                self.tree.column(col, width=120)

        # Скроллбары
        ysb = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, sticky="ew")

        # Растягивание
        self.tree_frame.rowconfigure(0, weight=1)
        self.tree_frame.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # Привязка событий
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<Double-1>", self.selection_stat)

    def _refresh_treeview(self):
        """Обновляет содержимое TreeView из списка self.persons"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for person in self.persons:
            self.tree.insert("", tk.END, values=(
                person.id,
                person.last_name,
                person.first_name,
                person.middle_name,
                person.gender,
                person.birth_date.strftime('%d.%m.%Y'),
                person.work_from.strftime('%d.%m.%Y')
            ))

    def _get_person_from_form(self, person_id=None):
        """Создает объект Person из данных формы"""
        last_name = self.entry1.get().strip()
        first_name = self.entry2.get().strip()
        middle_name = self.entry3.get().strip()
        gender = self.gender_var.get()
        birth_date = self.entry5.get_date()
        work_from = self.entry6.get_date()

        return Person(
            id=person_id if person_id else max((p.id for p in self.persons), default=0) + 1,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            gender=gender,
            birth_date=birth_date,
            work_from=work_from
        )

    def add_person(self):
        try:
            person = self._get_person_from_form()
            errors = PersonValidator.validate(person)
            if errors:
                mb.showwarning("Ошибки ввода", "\n".join(errors))
                return

            self.persons.append(person)
            self.repo.save_all(self.persons)
            self._refresh_treeview()
            self.clear_entries()
            mb.showinfo("Успех", "Сотрудник успешно добавлен")

        except Exception as e:
            mb.showerror("Ошибка", f"Не удалось добавить сотрудника: {str(e)}")

    def edit_person(self):
        selected = self.tree.selection()
        if not selected:
            mb.showwarning("Предупреждение", "Выберите сотрудника для редактирования")
            return

        try:
            item_index = self.tree.index(selected[0])
            old_person = self.persons[item_index]
            new_person = self._get_person_from_form(old_person.id)

            errors = PersonValidator.validate(new_person)
            if errors:
                mb.showwarning("Ошибки ввода", "\n".join(errors))
                return

            self.persons[item_index] = new_person
            self.repo.save_all(self.persons)
            self._refresh_treeview()
            mb.showinfo("Успех", "Данные сотрудника обновлены")

        except Exception as e:
            mb.showerror("Ошибка", f"Не удалось обновить данные: {str(e)}")

    def delete_person(self):
        selected = self.tree.selection()
        if not selected:
            mb.showwarning("Предупреждение", "Выберите сотрудника для удаления")
            return

        if not mb.askyesno("Подтверждение", "Вы уверены, что хотите удалить сотрудника?"):
            return

        try:
            item_index = self.tree.index(selected[0])
            del self.persons[item_index]
            self.repo.save_all(self.persons)
            self._refresh_treeview()
            self.clear_entries()
            mb.showinfo("Успех", "Сотрудник удален")

        except Exception as e:
            mb.showerror("Ошибка", f"Не удалось удалить сотрудника: {str(e)}")

    def clear_entries(self):
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.entry3.delete(0, tk.END)
        self.gender_var.set("М")
        today = date.today()
        self.entry5.set_date(today)
        self.entry6.set_date(today)

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        try:
            item_index = self.tree.index(selected[0])
            person = self.persons[item_index]

            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, person.last_name)

            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, person.first_name)

            self.entry3.delete(0, tk.END)
            self.entry3.insert(0, person.middle_name)

            self.gender_var.set(person.gender)

            self.entry5.set_date(person.birth_date)
            self.entry6.set_date(person.work_from)

        except Exception as e:
            mb.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def selection_stat(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        try:
            item_index = self.tree.index(selected[0])
            person = self.persons[item_index]
            report = PensionService.generate_report(person)
            mb.showinfo(title=person.get_short_name(), message=report)

        except Exception as e:
            mb.showerror("Ошибка", f"Не удалось сформировать отчет: {str(e)}")


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()