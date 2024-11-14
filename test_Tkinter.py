import tkinter as tk
from tkinter import messagebox, ttk

# Функция, которая будет вызываться при нажатии кнопки
def on_button_click():
    messagebox.showinfo("Информация", f"Привет, {entry.get()}!")

# Создаем главное окно
root = tk.Tk()
root.title("Пример Tkinter")

# Создаем метку
label = tk.Label(root, text="Введите Ваше имя:")
label.pack(pady=10)

# Создаем текстовое поле для ввода
entry = tk.Entry(root)
entry.pack(pady=10)

# Создаем кнопку
button = tk.Button(root, text="Нажми меня!", command=on_button_click)
button.pack(pady=10)

# Создаем флажок
check_var = tk.BooleanVar()
checkbutton = tk.Checkbutton(root, text="Согласен с условиями", variable=check_var)
checkbutton.pack(pady=10)

# Создаем выпадающий список
combo_box = ttk.Combobox(root, values=["Опция 1", "Опция 2", "Опция 3"])
combo_box.pack(pady=10)
combo_box.current(0)  # Устанавливаем первую опцию по умолчанию

# Создаем текстовую область
text_area = tk.Text(root, height=5, width=40)
text_area.pack(pady=10)

# Запускаем главный цикл приложения
root.mainloop()

#Как работает этот код:
#Импорт библиотек: Сначала мы импортируем необходимые модули из tkinter.

#Функция on_button_click: Эта функция вызывается, когда пользователь нажимает кнопку. Она показывает всплывающее окно с приветствием.

#Создание главного окна: Мы создаем объект Tk(), который является основным окном приложения.

#Добавление элементов:

#Метка для ввода имени,
#Текстовое поле для ввода,
#Кнопка, которая вызывает функцию при нажатии,
#Флажок для выбора,

#Выпадающий список с несколькими опциями,
#Текстовая область для ввода многострочного текста.
#Запуск цикла приложения: Вызов mainloop() запускает основной цикл событий Tkinter, который ожидает от пользователя действий.

import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Пример Tkinter")
        self.geometry("400x300")

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.label = ttk.Label(self.main_frame, text="Главное окно")
        self.label.pack(pady=10)

        self.button_open = ttk.Button(self.main_frame, text="Открыть фрейм", command=self.open_frame)
        self.button_open.pack(pady=10)

        self.button_quit = ttk.Button(self.main_frame, text="Выход", command=self.quit)
        self.button_quit.pack(pady=10)

    def open_frame(self):
        self.new_window = tk.Toplevel(self)
        self.new_window.title("Дополнительное окно")
        self.new_window.geometry("300x200")

        label = ttk.Label(self.new_window, text="Это дополнительное окно")
        label.pack(pady=10)

        button_close = ttk.Button(self.new_window, text="Закрыть", command=self.new_window.destroy)
        button_close.pack(pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
    
# Объяснение кода:
# Создаётся основное окно (App), в котором есть фрейм (main_frame).
# При нажатии на кнопку "Открыть фрейм" создаётся дополнительное окно (Toplevel).
# Каждое дополнительное окно можно закрыть с помощью кнопки "Закрыть".



