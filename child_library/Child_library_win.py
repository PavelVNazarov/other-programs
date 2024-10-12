# Child_library_win.py
# Назаров ПВ

import tkinter as tk
from tkinter import messagebox
import sqlite3

def setup_db():
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
            publishing TEXT)
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
    conn.commit()
    conn.close()

class LibraryApp:
    def __init__(self, root):
        self.root = root
        root.title("Библиотека")
        self.add_book_button = tk.Button(root, text="Добавить новую книгу", command=self.create_book_window)
        self.add_book_button.pack()

        self.show_books_button = tk.Button(root, text="Посмотреть все книги", command=self.show_books)
        self.show_books_button.pack()

        self.add_reader_button = tk.Button(root, text="Добавить нового читателя", command=self.add_reader_window)
        self.add_reader_button.pack()

        self.show_readers_button = tk.Button(root, text="Посмотреть всех читателей", command=self.show_readers)
        self.show_readers_button.pack()

        self.exit_button = tk.Button(root, text="Выход", command=root.quit)
        self.exit_button.pack()

    def show_books(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        conn.close()

        if books:
            message = "\n".join([f"{book[1]} - {book[2]}" for book in books])
            messagebox.showinfo("Все книги", message)
        else:
            messagebox.showinfo("Все книги", "Книги не найдены.")

    def add_reader_window(self):
        window = tk.Toplevel(self.root)
        window.title("Добавить читателя")
        
        tk.Label(window, text="Фамилия:").grid(row=0, column=0)
        famili_entry = tk.Entry(window)
        famili_entry.grid(row=0, column=1)

        tk.Label(window, text="Имя:").grid(row=1, column=0)
        name_entry = tk.Entry(window)
        name_entry.grid(row=1, column=1)

        tk.Label(window, text="Фамилия:").grid(row=2, column=0)
        surname_entry = tk.Entry(window)
        surname_entry.grid(row=2, column=1)

        tk.Label(window, text="Школа:").grid(row=3, column=0)
        school_entry = tk.Entry(window)
        school_entry.grid(row=3, column=1)

        tk.Label(window, text="Класс:").grid(row=4, column=0)
        class_num_entry = tk.Entry(window)
        class_num_entry.grid(row=4, column=1)

        tk.Label(window, text="Номер телефона:").grid(row=5, column=0)
        number_entry = tk.Entry(window)
        number_entry.grid(row=5, column=1)

        tk.Button(window, text="Добавить читателя", command=lambda: self.add_reader(famili_entry.get(), name_entry.get(), surname_entry.get(), school_entry.get(), class_num_entry.get(), number_entry.get())).grid(row=6, columnspan=2)

    def add_reader(self, famili, name, surname, school, class_num, number):
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO readers (famili, name, surname, school, class_num, number) VALUES (?, ?, ?, ?, ?, ?)",
                           (famili, name, surname, school, class_num, number))
            conn.commit()
            messagebox.showinfo("Успех", "Читатель успешно добавлен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить читателя: {e}")
        finally:
            conn.close()

    def show_readers(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM readers")
        readers = cursor.fetchall()
        conn.close()
        
        if readers:
            message = "\n".join([f"{reader[1]} {reader[2]} {reader[3]}" for reader in readers])
            messagebox.showinfo("Все читатели", message)
        else:
            messagebox.showinfo("Все читатели", "Читатели не найдены.")

    def create_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Добавить книгу")

        tk.Label(window, text="Автор:").grid(row=0, column=0)
        autor_entry = tk.Entry(window)
        autor_entry.grid(row=0, column=1)

        tk.Label(window, text="Название:").grid(row=1, column=0)
        name_entry = tk.Entry(window)
        name_entry.grid(row=1, column=1)

        tk.Label(window, text="Номер в каталоге:").grid(row=2, column=0)
        number_entry = tk.Entry(window)
        number_entry.grid(row=2, column=1)

        tk.Label(window, text="Издательство:").grid(row=3, column=0)
        publishing_entry = tk.Entry(window)
        publishing_entry.grid(row=3, column=1)

        tk.Label(window, text="Год издания:").grid(row=4, column=0)
        publication_entry = tk.Entry(window)
        publication_entry.grid(row=4, column=1)

        tk.Label(window, text="Аннотация:").grid(row=5, column=0)
        annot_entry = tk.Entry(window)
        annot_entry.grid(row=5, column=1)

        tk.Button(window, text="Добавить книгу", command=lambda: self.add_book(autor_entry.get(), name_entry.get(), number_entry.get(), publishing_entry.get(), publication_entry.get(), annot_entry.get())).grid(row=6, columnspan=2)

    def add_book(self, autor, name, number, publishing, publication, annot):
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO books (autor, name, annot, number, publication, publishing) VALUES (?, ?, ?, ?, ?, ?)',
                           (autor, name, annot, number, publication, publishing))
            conn.commit()
            messagebox.showinfo("Успех", "Книга успешно добавлена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить книгу: {e}")
        finally:
            conn.close()

# Запуск программы
if __name__ == "__main__":
    setup_db()
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
