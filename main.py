#импорт
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3

#класс приложения
class EmployeeManagementApp:

    #заголовки
    def __init__(self, master):
        self.master = master
        self.master.title('Список сотрудников компании')

        self.conn = sqlite3.connect('employees.db')
        self.create_table()

        self.tree = ttk.Treeview(master)
        self.tree['columns'] = ('ID', 'Name', 'Phone', 'Email', 'Salary')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='ФИО')
        self.tree.heading('Phone', text='Номер телефона')
        self.tree.heading('Email', text='Почта')
        self.tree.heading('Salary', text='Зарплата')
        self.tree.pack(padx=20, pady=20)

        self.create_widgets()
        self.update_treeview()

    #создание БД
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                email TEXT,
                salary INTEGER
            )
        ''')
        self.conn.commit()

    #создание виджетов
    def create_widgets(self):
        self.add_button = tk.Button(self.master, text='Добавить сотрудника', command=self.add_employee)
        self.add_button.pack(pady=10)
        self.update_button = tk.Button(self.master, text='Обновить данные сотрудника', command=self.update_employee)
        self.update_button.pack(pady=10)
        self.delete_button = tk.Button(self.master, text='Удалить сотрудника', command=self.delete_employee)
        self.delete_button.pack(pady=10)
        self.search_button = tk.Button(self.master, text='Найти сотрудника', command=self.search_employee)
        self.search_button.pack(pady=10)

    #функция виджета 'добавить сотрудника'
    def add_employee(self):
        name = simpledialog.askstring('Ввод', 'Введите ФИО сотрудника:')
        phone = simpledialog.askstring('Ввод', 'Введите номер сотрудника:')
        email = simpledialog.askstring('Ввод', 'Введите email сотрудника:')
        salary = simpledialog.askinteger('Ввод', 'Введите зарплату сотрудника:')

        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)', (name, phone, email, salary))
        self.conn.commit()
        self.update_treeview()
        self.last_action = 'Добавить'

    #функция виджета 'обновить сотрудника'
    def update_employee(self):
        emp_id = simpledialog.askinteger('Ввод', 'Введите ID сотрудника:')

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE id=?', (emp_id,))
        employee = cursor.fetchone()

        if employee:
            name = simpledialog.askstring('Ввод', 'Введите новое ФИО сотрудника:', initialvalue=employee[1])
            phone = simpledialog.askstring('Ввод', 'Введите новый номер сотрудника:', initialvalue=employee[2])
            email = simpledialog.askstring('Ввод', 'Введите новый email сотрудника:', initialvalue=employee[3])
            salary = simpledialog.askinteger('Ввод', 'Введите новую зарплату сотрудника:', initialvalue=employee[4])

            cursor.execute('UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?', (name, phone, email, salary, emp_id))
            self.conn.commit()
            self.update_treeview()
            self.last_action = 'Обновить'
        else:
            messagebox.showerror('Ошибка', 'Сотрудник не найден.')

    #функция виджета 'удалить сотрудника'
    def delete_employee(self):
        emp_id = simpledialog.askinteger('Ввод', 'Введите ID сотрудника:')

        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM employees WHERE id=?', (emp_id,))
        self.conn.commit()
        self.update_treeview()
        self.last_action = 'Удалить'

    #функция виджета 'найти сотрудника'
    def search_employee(self):
        name = simpledialog.askstring('Ввод', 'Введите ФИО сотрудника:')

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE name=?', (name,))
        employees = cursor.fetchall()

        if employees:
            self.tree.delete(*self.tree.get_children())
            for employee in employees:
                self.tree.insert('', 'end', values=employee)
        else:
            messagebox.showinfo('Информация', 'Сотрудник с данным именем не найден.')

    #обновление treeview
    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()

        for employee in employees:
            self.tree.insert('', 'end', values=employee)

    #действия при закрытии
    def on_closing(self):
        self.conn.close()
        self.master.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.protocol('WM_DELETE_WINDOW', app.on_closing)
    root.mainloop()