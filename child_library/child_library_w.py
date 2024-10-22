import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
import hashlib

# Функция для хеширования пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Проверка пароля
def check_password():
    input_password = password_entry.get()
    if hash_password(input_password) == stored_hashed_password:
        admin_button.pack()
    else:
        password_label.config(text="Неверный пароль!")

# Создание главного окна
root = tk.Tk()
root.title("Библиотека")
root.geometry("800x600")
root.resizable(False, False)

# Подключаемся к БД
connection = sqlite3.connect('library.db')
cursor = connection.cursor()

# Храненый хеш пароля
stored_hashed_password = hash_password("l1i2b3r4a5r6y7")

# Создание вкладок
tab_control = ttk.Notebook(root)

# Вкладка "Главная"
main_tab = ttk.Frame(tab_control)
tab_control.add(main_tab, text='Главная')

# Показ изображения на главной вкладке
def show_image():
    img = Image.open("path/to/image.jpg")  # Замените на путь к изображению
    img = img.resize((300, 200))  # Измените размер по необходимости
    img_tk = ImageTk.PhotoImage(img)

    img_label = tk.Label(main_tab, image=img_tk)
    img_label.image = img_tk  # Сохраняем ссылку на изображение
    img_label.pack()

show_image()

# Вкладка "Книги"
books_tab = ttk.Frame(tab_control)
tab_control.add(books_tab, text='Книги')

find_book_button = tk.Button(books_tab, text="Найти книгу")
find_book_button.pack(pady=10)

new_book_button = tk.Button(books_tab, text="Новая книга")
new_book_button.pack(pady=10)

# Вкладка "Читатели"
readers_tab = ttk.Frame(tab_control)
tab_control.add(readers_tab, text='Читатели')

new_reader_button = tk.Button(readers_tab, text="Новый читатель")
new_reader_button.pack(pady=10)

find_reader_button = tk.Button(readers_tab, text="Найти читателя")
find_reader_button.pack(pady=10)

# Вкладка "Библиотека"
library_tab = ttk.Frame(tab_control)
tab_control.add(library_tab, text='Библиотека')

library_img = Image.open("path/to/library_image.jpg")  # Замените на путь к изображению
library_img = library_img.resize((300, 200))  # Измените размер по необходимости
library_img_tk = ImageTk.PhotoImage(library_img)

library_img_label = tk.Label(library_tab, image=library_img_tk)
library_img_label.image = library_img_tk  # Сохраняем ссылку на изображение
library_img_label.pack()

library_info_label = tk.Label(library_tab, text="Здравствуйте, здесь будет краткая информация о нашей библиотеке.")
library_info_label.pack(pady=10)

about_us_button = tk.Button(library_tab, text="О нас")
about_us_button.pack(pady=5)

librarians_button = tk.Button(library_tab, text="Библиотекари")
librarians_button.pack(pady=5)

# Вкладка "Администратор"
admin_tab = ttk.Frame(tab_control)
tab_control.add(admin_tab, text='Администратор')

password_label = tk.Label(admin_tab, text="Введите пароль:")
password_label.pack(pady=10)

password_entry = tk.Entry(admin_tab, show='*')
password_entry.pack(pady=10)

check_password_button = tk.Button(admin_tab, text="Проверить пароль", command=check_password)
check_password_button.pack(pady=10)

admin_button = tk.Button(admin_tab, text="Сотрудники")
admin_button.pack(pady=10)
admin_button.pack_forget()  # Скрываем кнопку до проверки пароля

tab_control.pack(expand=1, fill='both')

root.mainloop()
