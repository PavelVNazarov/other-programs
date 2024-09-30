
# Назаров ПВ
# Каталог читателей

from random import randint
import os

Lib_file_name = 'child_library'
Lib_readers = [] # список всех читателей
Lib_books = [] # список всех книг библиотеки - каталог
curent_reader = None # чей формуляр открыт

# 1 - новая книга
# 2 - новый читатель
# 3 - посмотреть формуляр читателя
# 4 - вписать книгу в формуляр
# 5 - отметить возврат книги
# 6 - изменить данные в формуляре

class book:
    def __init__(self):
        self.name : str # название
        self.autor : str # автор
        self.annot : str # аннотация
        self.number : int # номер в каталоге
        self.publication : int # год издания
        self.publishing : str # издательство

    def new_book(self):
        self.autor = input('Автор киги (авторы): ')
        self.name = input('Название: ')
        self.number = input('Номер в библиотечном каталоге: ')
        self.publishig = input('Издательство: ')
        self.publication = input('Год издания: ')
        self.annot = input('Аннотация: ')
        book_new = book(self)
        Lib_books.append(book_new)
        
class reader:
    def __init__(self):
        self.name : str # имя
        self.surname : str # отчество
        self.famili : str # фамилия
        self.class_num : str # класс
        self.school : str # школа
        self.books = [] # книги
        self.number : int # номер формуляра
        
    def __str__(self):
        print(curent_reader.famili, curent_reader.name, curent_reader.surname, curent_reader.school, curent_reader.class_num, curent_reader.number)

    def new_reader(self):
        self.famili = input('Фамилия: ')
        self.name = input('Имя: ')
        self.surname = input('Отчество: ')
        self.school = input('Школа: ')
        self.class_num = input('Класс: ')
        self.number = input('Номер формуляра: ')
        reader_new = reader(self)
        Lib_readers.append(reader_new)
        curent_reader = reader_new

    def reader_form_read(self):
        if curent_reader == None:
            print('Сначала откройте формуляр читателя!')
            self.famili = input('Фамилия: ')
            self.name = input('Имя: ')
            self.surname = input('Отчество: ')
            self.school = input('Школа: ')
            self.class_num = input('Класс: ')
            self.number = input('Номер формуляра: ')
            reader_new = reader(self)
            curent_reader = reader_new
            start_prog()
        else:
            print(curent_reader)
        
    
    def reader_book_write(self):
        if curent_reader == None:
            print('Сначала откройте формуляр читателя!')
            reader.reader_form_read()
    
    def reader_book_return(self):
        if curent_reader == None:
            print('Сначала откройте формуляр читателя!')
            reader.reader_form_read()
    
    def reader_form_write(self):
        if curent_reader == None:
            print('Сначала откройте формуляр читателя!')
            reader.reader_form_read()

def start_prog():

    print('Вас приветствует детская библиотека!')
    print()
    print('1 - новая книга')
    print('2 - новый читатель')
    print('3 - посмотреть формуляр читателя')
    print('4 - вписать книгу в формуляр')
    print('5 - отметить возврат книги')
    print('6 - изменить данные в формуляре')
    act_num = input()
        match act_num:
        case 1:
            book.new_book()
        case 2:
            reader.new_reader()
        case 3:
            reader.reader_form_read()
        case 4:
            reader.reader_book_write()
        case 5:
            reader.reader_book_return()
        case 6:
            reader.reader_form_write()



start_prog()
