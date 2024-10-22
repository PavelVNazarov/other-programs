import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
import hashlib

# Создание базы данных и таблиц
def create_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS readers (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

# Функции для добавления книг и читателей
def add_book(title):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title) VALUES (?)", (title,))
    conn.commit()
    conn.close()

def add_reader(name):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO readers (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

# Функции для отображения всех книг и читателей
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

# Проверка пароля
def check_password(input_password):
    hashed_password = hashlib.sha256(input_password.encode()).hexdigest()
    return hashed_password == hashlib.sha256("l1i2b3r4a5r6y7".encode()).hexdigest()

# Основное окно
root = tk.Tk()
root.title("Библиотека")
root.geometry("800x600")
root.resizable(False, False)

# Создание вкладок
tab_control = ttk.Notebook(root)

# Вкладка "Главная"
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Главная')

# Вкладка "Читатели"
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Читатели')

# Вкладка "Книги"
tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='Книги')

# Вкладка "Библиотека"
tab4 = ttk.Frame(tab_control)
tab_control.add(tab4, text='Библиотека')

# Вкладка "Администратор"
tab5 = ttk.Frame(tab_control)
tab_control.add(tab5, text='Администратор')

tab_control.pack(expand=1, fill='both')

# Добавление изображений на вкладки
def load_image(tab, image_path):
    img = Image.open(image_path)
    img = img.resize((200, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    label = tk.Label(tab, image=img)
    label.image = img  # Сохраняем ссылку на изображение
    label.pack(side=tk.TOP)

load_image(tab1, 'main_image.png')  # Замените на путь к Вашей картинке
load_image(tab2, 'readers_image.png')  # Замените на путь к Вашей картинке
load_image(tab3, 'books_image.png')  # Замените на путь к Вашей картинке
load_image(tab4, 'library_image.png')  # Замените на путь к Вашей картинке
load_image(tab5, 'admin_image.png')  # Замените на путь к Вашей картинке

# Кнопки на вкладке "Книги"
def add_book_button():
    add_book("Новая книга")  # Здесь можно добавить ввод от пользователя

def show_books_button():
    books = show_books()
    messagebox.showinfo("Книги", "\n".join([book[1] for book in books]))

tk.Button(tab3, text="Новая книга", command=add_book_button).pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(tab3, text="Показать книги", command=show_books_button).pack(side=tk.LEFT, padx=10, pady=10)

# Кнопки на вкладке "Читатели"
def add_reader_button():
    add_reader("Новый читатель")  # Здесь можно добавить ввод от пользователя

def show_readers_button():
    readers = show_readers()
    messagebox.showinfo("Читатели", "\n".join([reader[1] for reader in readers]))

tk.Button(tab2, text="Новый читатель", command=add_reader_button).pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(tab2, text="Показать читателей", command=show_readers_button).pack(side=tk.LEFT, padx=10, pady=10)

# Вкладка "Библиотека"
tk.Label(tab4, text="Здравствуйте, здесь будет краткая информация о нашей библиотеке.").pack(side=tk.TOP, pady=10)
tk.Button(tab4, text="О нас").pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(tab4, text="Библиотекари").pack(side=tk.LEFT, padx=10, pady=10)

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
