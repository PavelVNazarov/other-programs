
# Назаров ПВ
# Каталог читателей

from random import randint
import os

Lib_file_name = 'child_library'
Lib_readers = [] # список всех читателей
Lib_books = [] # список всех книг библиотеки - каталог


# 1 - новая книга
# 2 - новый читатель
# 3 - посмотреть формуляр читателя
# 4 - вписать книгу в формуляр
# 5 - отметить возврат книги
# 6 - изменить данные в формуляре

class book:
    def __init__(self, autor = ' ',
                       name = ' ',
                       annot = ' ',
                       number = ' ',
                       publication = 2000,
                       publishing = ' '):
        self.name = name # название
        self.autor = autor # автор
        self.annot = annot # аннотация
        self.number = number # номер в каталоге
        self.publication = publication # год издания
        self.publishing = publishing # издательство

    def new_book():
        autor = input('Автор киги (авторы): ')
        name = input('Название: ')
        number = input('Номер в библиотечном каталоге: ')
        publishing = input('Издательство: ')
        publication = int(input('Год издания: '))
        annot = input('Аннотация: ')
        book_new = book(autor, name, annot, number, publication, publishing)
        Lib_books.append(book_new)

class reader:
    curent_reader = None  # чей формуляр открыт

    def __init__(self, surname = ' ',
                       name = ' ',
                       famili = ' ',
                       number = 0,
                       class_num = ' ',
                       school = ' '):
        self.name = name # имя
        self.surname = surname # отчество
        self.famili = famili # фамилия
        self.class_num = class_num # класс
        self.school = school # школа
        self.number = number # номер формуляра
        self.books = []  # книги

    def __str__(self):
        print(reader.curent_reader.famili,
              reader.curent_reader.name,
              reader.curent_reader.surname,
              reader.curent_reader.school,
              reader.curent_reader.class_num,
              reader.curent_reader.number)

    def new_reader():
        famili = input('Фамилия: ')
        name = input('Имя: ')
        surname = input('Отчество: ')
        school = int(input('Школа: '))
        class_num = input('Класс: ')
        number = input('Номер формуляра: ')
        if input('Всё правильно, регистрируем? д - да / н - нет: ') == ('д' or 'Д'):
            reader.curent_reader = reader(famili, name, surname, school, class_num, number)
            Lib_readers.append(reader.curent_reader)
            if input('Еще один читатель? д - да / н - нет: ') == ('д' or 'Д'):
                reader.new_reader()
            else:
                start_prog()
        else:
            if input('Попробуем снова? д - да / н - нет: ') == ('д' or 'Д'):
                reader.new_reader()
            else:
                start_prog()

    def reader_form_read():
        if reader.curent_reader == None:
            print('Формуляр читателя!')
            famili = input('Фамилия: ')
            name = input('Имя: ')
            surname = input('Отчество: ')
            school = int(input('Школа: '))
            class_num = input('Класс: ')
            number = input('Номер формуляра: ')
            reader_new = reader(famili, name, surname, school, class_num, number)
            if reader.try_reader(reader_new):
                reader.curent_reader = reader_new
            start_prog()
        else:
            print(reader.curent_reader)

    def try_reader(self):
        # проверка читателя через каталог читателей
        return True

    def reader_book_write():
        if reader.curent_reader == None:
            print('Сначала откройте формуляр читателя!')
            reader.reader_form_read()
        else:
            print(reader.curent_reader)

    def reader_book_return():
        if reader.curent_reader == None:
            print('Сначала откройте формуляр читателя!')
            reader.reader_form_read()
        else:
            print(reader.curent_reader)

    def reader_form_write():
        if reader.curent_reader == None:
            print('Сначала откройте формуляр читателя!')
            reader.reader_form_read()
        else:
            new_famili = input(f'Фамилия: {reader.curent_reader.famili} ?')
            if new_famili != '':
                reader.curent_reader.famili = new_famili

            new_name = input(f'Имя: {reader.curent_reader.name} ?')
            if new_name != '':
                reader.curent_reader.name = new_name

            new_surname = input(f'Отчество: {reader.curent_reader.surname} ?')
            if new_surname != '':
                reader.curent_reader.surname = new_surname

            new_school = input(f'Школа: {reader.curent_reader.school} ?')
            if new_school != '':
                reader.curent_reader.school = new_school

            new_class_num = input(f'Класс: {reader.curent_reader.class_num} ?')
            if new_class_num  != '':
                reader.curent_reader.class_num  = new_class_num

            new_number = input(f'Номер формуляра: {reader.curent_reader.number} ?')
            if new_number != '':
                reader.curent_reader.number = new_number

            print(reader.curent_reader)

def start_prog():

    print('Вас приветствует детская библиотека!')
    print()
    print('1 - новая книга')
    print('2 - новый читатель')
    if reader.curent_reader != None:
        print(reader.curent_reader)
        print('3 - посмотреть формуляр читателя')
        print('4 - вписать книгу в формуляр')
        print('5 - отметить возврат книги')
        print('6 - изменить данные читателя в формуляре')
    act_num = input('? ')
    if act_num == '1':
        book.new_book()
    if act_num == '2':
        reader.new_reader()
    if act_num == '3':
        reader.reader_form_read()
    if act_num == '4':
        reader.reader_book_write()
    if act_num == '5':
        reader.reader_book_return()
    if act_num == '6':
        reader.reader_form_write()
    print(act_num)


start_prog()
