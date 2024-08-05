class User:
  """
  Класс пользователь, содержащий атрибуты: логин и пароль
  """
  def __init__(self, username, pasword, pasword_confirm):
    self.username = username
    if pasword == pasword_confirm:
      self.pasword = pasword
      
class DataBase:
  def __init__(self):
    self.data = {}

  def add_user(self, username,pasword):
    self.data[username] = pasword


if __name__ == '__main__':
  database = DataBase()
  while True:
    choice = input("Приветствую! Выберите действие: \n1 - Вход\n2 - Регистрация\n")
    if choice == 1:
      login = input("Введите логин: ")
      pasword = input("Введите пароль: ")
      if login in database.data:
        if pasword == database.data[login]:
          print(f"Вы вошли в систему, {login}")
          break
        else:
          print("Неверный пароль")
      else:
        print("Неверный логин или пароль")
    if choice == 2:
      user = User(input("Введите логин: "),
                  pasword := input("Введите пароль: "),
                  pasword2 := input("Повторите пароль: "))
      if pasword != pasword2:
        print(f"Пароли не совпадают")
        continue
      database.add_user(user.username, user.pasword)
    print(database.data)

