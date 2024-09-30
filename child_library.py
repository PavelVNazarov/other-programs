
# Назаров ПВ
# Каталог читателей

from random import randint
import os

file_name = 'child_library'

class book:
    def __init__(self):
        self.name : str # название
        self.autor : str # автор
        self.annot : str # аннотация
        self.number : int # номер в каталоге
        self.publication : int # год издания
        self.publishing : str # издательство

class reader:
    def __init__(self):
        self.name : str # имя
        self.surname : str # отчество
        self.famile : str # фамилия
        self.class_num : str # класс
        self.school : str # школа
        self.books = [] # книги
        self.number : int # номер формуляра

# 1 - новая книга
# 2 - новый читатель
# 3 - посмотреть формуляр читателя
# 4 - вписать книгу в формуляр
# 5 - отметить возврат книги
# 6 - изменить данные в формуляре
