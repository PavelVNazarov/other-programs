import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib

class BorrowedBook:
    def __init__(self, reader_id, book_id, issue_date, return_due_date, actual_return_date=None):
        self.reader_id = reader_id
        self.book_id = book_id
        self.issue_date = issue_date
        self.return_due_date = return_due_date
        self.actual_return_date = actual_return_date

    def add_borrowed_book_to_db(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO borrowed_books (reader_id, book_id, issue_date, return_due_date, actual_return_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.reader_id, self.book_id, self.issue_date, self.return_due_date, self.actual_return_date))
        conn.commit()
        conn.close()


def create_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            autor TEXT, 
            name TEXT, 
            annot TEXT,
            number TEXT, 
            publication INTEGER, 
            publishing TEXT,
            pages INTEGER,
            copies INTEGER,
            status TEXT)  -- может хранить значения: 'в библиотеке', 'у читателя', 'списана', 'утеряна'
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readers (
            id INTEGER PRIMARY KEY,
            famili TEXT, 
            name TEXT, 
            surname TEXT,
            school TEXT,
            class_num TEXT,
            number TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY,
            reader_id INTEGER,
            book_id INTEGER,
            issue_date TEXT,
            due_date TEXT,
            return_date TEXT,
            FOREIGN KEY (reader_id) REFERENCES readers (id),
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')

    conn.commit()
    conn.close()

def add_book_button():
    window = tk.Toplevel(root)
    window.title("Добавить книгу")

    frame = ttk.Frame(window)
    frame.pack(padx=10, pady=10)

    tk.Label(frame, text="Автор:").grid(row=0, column=0)
    autor_entry = tk.Entry(frame)
    autor_entry.grid(row=0, column=1)

    tk.Label(frame, text="Название:").grid(row=1, column=0)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=1, column=1)

    tk.Label(frame, text="Количество страниц:").grid(row=2, column=0)
    pages_entry = tk.Entry(frame)
    pages_entry.grid(row=2, column=1)

    tk.Label(frame, text="Количество экземпляров:").grid(row=3, column=0)
    copies_entry = tk.Entry(frame)
    copies_entry.grid(row=3, column=1)

    tk.Label(frame, text="Номер в каталоге:").grid(row=4, column=0)
    number_entry = tk.Entry(frame)
    number_entry.grid(row=4, column=1)

    tk.Button(frame, text="Добавить", command=lambda: add_book(autor_entry.get(), name_entry.get(),
                                                              pages_entry.get(), copies_entry.get(),
                                                              number_entry.get())).grid(row=5, columnspan=2, pady=10)

def add_book(title):
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO books (autor, name, annot, number, publication, publishing, pages, copies, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (autor, name, annot, number, publication, publishing, pages, copies, status))
        conn.commit()
        messagebox.showinfo("Успех", "Книга успешно добавлена!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось добавить книгу: {e}")
    finally:
        conn.close()


def add_reader(name):
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO readers (famili, name, surname, school, class_num, number, borrowed_books) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (famili, name, surname, school, class_num, number, json.dumps(borrowed_books))) # Здесь borrowed_books должен быть списком строк
        conn.commit()
        messagebox.showinfo("Успех", "Читатель успешно добавлен!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось добавить читателя: {e}")
    finally:
        conn.close()

def show_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def show_readers():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM readers")
    readers = cursor.fetchall()
    conn.close()
    return readers

def add_book_button():
    window = tk.Toplevel(root)
    window.title("Добавить книгу")

    frame = ttk.Frame(window)
    frame.pack(padx=10, pady=10)

    tk.Label(frame, text="Автор:").grid(row=0, column=0)
    autor_entry = tk.Entry(frame)
    autor_entry.grid(row=0, column=1)

    tk.Label(frame, text="Название:").grid(row=1, column=0)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=1, column=1)

    tk.Label(frame, text="Аннотация:").grid(row=2, column=0)
    annot_entry = tk.Entry(frame)
    annot_entry.grid(row=2, column=1)

    tk.Label(frame, text="Номер в каталоге:").grid(row=3, column=0)
    number_entry = tk.Entry(frame)
    number_entry.grid(row=3, column=1)

    tk.Button(frame, text="Добавить", command=lambda: add_book(autor_entry.get(), name_entry.get(), annot_entry.get(), number_entry.get(), 2023, "Publishing House")).grid(row=4, columnspan=2, pady=10)

def show_books_button():
    books = show_books()
    if books:
        message = "\n".join([f"{book[1]} - {book[2]}" for book in books])
        messagebox.showinfo("Книги", message)
    else:
        messagebox.showinfo("Книги", "Книги не найдены.")

def add_reader_button():
    window = tk.Toplevel(root)
    window.title("Добавить читателя")

    frame = ttk.Frame(window)
    frame.pack(padx=10, pady=10)

    tk.Label(frame, text="Фамилия:").grid(row=0, column=0)
    famili_entry = tk.Entry(frame)
    famili_entry.grid(row=0, column=1)

    tk.Label(frame, text="Имя:").grid(row=1, column=0)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=1, column=1)

    tk.Label(frame, text="Отчество:").grid(row=2, column=0)
    surname_entry = tk.Entry(frame)
    surname_entry.grid(row=2, column=1)

    tk.Label(frame, text="Школа:").grid(row=3, column=0)
    school_entry = tk.Entry(frame)
    school_entry.grid(row=3, column=1)

    tk.Label(frame, text="Класс:").grid(row=4, column=0)
    class_num_entry = tk.Entry(frame)
    class_num_entry.grid(row=4, column=1)

    tk.Label(frame, text="Номер:").grid(row=5, column=0)
    number_entry = tk.Entry(frame)
    number_entry.grid(row=5, column=1)

    tk.Button(frame, text="Добавить", command=lambda: add_reader(famili_entry.get(), name_entry.get(), surname_entry.get(), school_entry.get(), class_num_entry.get(), number_entry.get())).grid(row=6, columnspan=2, pady=10)

def show_readers_button():
    readers = show_readers()
    if readers:
        message = "\n".join([f"{reader[1]} {reader[2]} {reader[3]}" for reader in readers])
        messagebox.showinfo("Читатели", message)
    else:
        messagebox.showinfo("Читатели", "Читатели не найдены.")


def issue_book(reader_id, book_id):
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # Добавить запись в таблицу loans
        issue_date = "2023-01-01"  # Замените на текущую дату
        due_date = "2023-01-11"  # Замените на текущую дату + 10 дней
        cursor.execute(
            "INSERT INTO loans (reader_id, book_id, issue_date, due_date) VALUES (?, ?, ?, ?)",
            (reader_id, book_id, issue_date, due_date)
        )

        # Обновить статус книги
        cursor.execute(
            "UPDATE books SET status = 'у читателя' WHERE id = ?",
            (book_id,)
        )

        conn.commit()
        messagebox.showinfo("Успех", "Книга выдана читателю!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось выдать книгу: {e}")
    finally:
        conn.close()


def return_book(loan_id):
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # Получить информацию по займу
        cursor.execute("SELECT book_id FROM loans WHERE id = ?", (loan_id,))
        book_id = cursor.fetchone()[0]

        # Обновить дату возврата в таблице loans
        return_date = "2023-01-05"  # Замените на текущую дату
        cursor.execute(
            "UPDATE loans SET return_date = ? WHERE id = ?",
            (return_date, loan_id)
        )

        # Обновить статус книги
        cursor.execute(
            "UPDATE books SET status = 'в библиотеке' WHERE id = ?",
            (book_id,)
        )

        conn.commit()
        messagebox.showinfo("Успех", "Книга возвращена!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось вернуть книгу: {e}")
    finally:
        conn.close()

def check_password(input_password):
    hashed_password = hashlib.sha256(input_password.encode()).hexdigest()
    return hashed_password == hashlib.sha256("l1i2b3r4a5r6y7".encode()).hexdigest()

root = tk.Tk()
root.title("Библиотека")
root.geometry("800x600")
root.resizable(False, False)

tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Главная')
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Читатели')
tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='Книги')
tab4 = ttk.Frame(tab_control)
tab_control.add(tab4, text='Библиотека')
tab5 = ttk.Frame(tab_control)
tab_control.add(tab5, text='Администратор')

tab_control.pack(expand=1, fill='both')

# Кнопки на вкладке "Книги"
tk.Button(tab3, text="Новая книга", command=add_book_button).pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(tab3, text="Показать книги", command=show_books_button).pack(side=tk.LEFT, padx=10, pady=10)

# Кнопки на вкладке "Читатели"
tk.Button(tab2, text="Новый читатель", command=add_reader_button).pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(tab2, text="Показать читателей", command=show_readers_button).pack(side=tk.LEFT, padx=10, pady=10)

# Вкладка "Библиотека"
tk.Label(tab4, text="Здравствуйте, здесь будет краткая информация о нашей библиотеке.").pack(side=tk.TOP, pady=10)
tk.Button(tab4, text="О нас").pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(tab4, text="Библиотекари").pack(side=tk.LEFT, padx=10, pady=10)

# Вкладка для управления выданными книгами
tab_loans = ttk.Frame(tab_control)
tab_control.add(tab_loans, text='Выданные книги')

# Обратите внимание, что это просто шаблон
tk.Button(tab_loans, text="Выдать книгу", command=lambda: issue_book(reader_id, book_id)).pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(tab_loans, text="Вернуть книгу", command=lambda: return_book(loan_id)).pack(side=tk.LEFT, padx=10, pady=10)



# Вкладка "Администратор"
def admin_login():
    password = password_entry.get()
    if check_password(password):
        tk.Button(tab5, text="Сотрудники").pack(side=tk.LEFT, padx=10, pady=10)
    else:
        messagebox.showerror("Ошибка", "Неверный пароль")

password_entry = tk.Entry(tab5, show='*')
password_entry.pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(tab5, text="Вход", command=admin_login).pack(side=tk.LEFT, padx=10, pady=10)

# Создание базы данных
create_db()

root.mainloop()
