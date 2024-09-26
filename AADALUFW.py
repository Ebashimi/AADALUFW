import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import subprocess
import sqlite3 as sq

# ЭКСПОРТ ДАННЫХ ИЗ SQLlite-ТАБЛИЦЫ

# Подключаемся к базе данных SQLite
with sq.connect("AllUserServer.db") as con:

    con.row_factory = sq.Row # Устанавливаем фабрику строк для доступа по именам столбцов
    cur = con.cursor() # Создаем курсор для выполнения SQL-запросов
    # Создаем таблицу, если она не существует
    cur.execute("""CREATE TABLE IF NOT EXISTS UserServer (
    UserName TEXT NOT NULL,
    UserPassword TEXT NOT NULL)""")
    # Извлекаем всех пользователей из базы данных
    cur.execute('SELECT * FROM UserServer')

class Ui_Osnova(object):

    def setupUi(self, Osnova):

        # Настройка основного окна приложения
        Osnova.setObjectName("Osnova")
        Osnova.resize(240, 320) # Устанавливаем размер окна
        Osnova.setMinimumSize(QtCore.QSize(240, 320)) # Минимальный размер окна
        Osnova.setMaximumSize(QtCore.QSize(240, 320)) # Максимальный размер окна

        # Создаем виджет для вертикального расположения элементов
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=Osnova)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 10, 221, 301))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")


        # 1. Кнопка создание пользователей
        self.CreateUsers = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.CreateUsers.setObjectName("CreateUsers")
        self.CreateUsers.clicked.connect(self.Create_Users)
        self.verticalLayout.addWidget(self.CreateUsers)

        # 2. Кнопка добавление в локальную группу
        self.AddLocalGroup = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.AddLocalGroup.setObjectName("AddLocalGroup")
        self.AddLocalGroup.clicked.connect(self.Add_Local_Group)
        self.verticalLayout.addWidget(self.AddLocalGroup)

        # 3. Кнопка удалить пользователей из группы
        self.DeleteLocalGroup = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.DeleteLocalGroup.setObjectName("DeleteLocalGroup")
        self.DeleteLocalGroup.clicked.connect(self.Delete_Local_Group)
        self.verticalLayout.addWidget(self.DeleteLocalGroup)

        # 4. Кнопка удалить пользователей
        self.DeleteUsers = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.DeleteUsers.setObjectName("DeleteUsers")
        self.DeleteUsers.clicked.connect(self.Delete_Users)
        self.verticalLayout.addWidget(self.DeleteUsers)

        self.retranslateUi(Osnova)
        QtCore.QMetaObject.connectSlotsByName(Osnova)

    def retranslateUi(self, Osnova):
        _translate = QtCore.QCoreApplication.translate
        Osnova.setWindowTitle(_translate("Osnova", "ALL USERS"))
        self.CreateUsers.setText(_translate("Osnova", "1. Создание пользователей"))
        self.AddLocalGroup.setText(_translate("Osnova", "2. Добавление в локальную группу"))
        self.DeleteLocalGroup.setText(_translate("Osnova", "3. Удаление из локальной группы"))
        self.DeleteUsers.setText(_translate("Osnova", "4. Удаление пользователей"))

    # 1. Функция для создания локальных пользователей
    def Create_Users(self):

        cur.execute('SELECT * FROM UserServer')

        for result in cur:
            username = result['UserName']
            userpassword = result['UserPassword']
            create_form_add_user = str('net user ' + username + ' ' + userpassword + ' /add')
            add_user = subprocess.Popen(['powershell', create_form_add_user])
            print("Пользователь: ", username, " Пароль: ", userpassword, " создан")

    # 2. Функция добавления пользователей в локальную группу "Пользователи удаленного рабочего стола"
    def Add_Local_Group(self):

        cur.execute('SELECT * FROM UserServer')

        for result in cur:
            username = result['UserName']
            userpassword = result['UserPassword']
            create_form_add_local_group = str(
                'net localgroup \"Пользователи удаленного рабочего стола\" ' + username + ' /add')
            add_local_group = subprocess.Popen(['powershell', create_form_add_local_group])
            print("Пользователь: ", username, " Пароль: ", userpassword, " добавлен")

    # 3. Функция удаления пользователей из локальной группы "Пользователи удаленного рабочего стола"
    def Delete_Local_Group(self):

        cur.execute('SELECT * FROM UserServer')

        for result in cur:
            username = result['UserName']
            userpassword = result['UserPassword']
            create_form_delete_local_group = str(
                'net localgroup \"Пользователи удаленного рабочего стола\" ' + username + ' /delete')
            delete_local_group = subprocess.Popen(['powershell', create_form_delete_local_group])
            print("Пользователь: ", username, " Пароль: ", userpassword, " убран")

    # 4 Функция для удаления локальных пользователей
    def Delete_Users(self):

        cur.execute('SELECT * FROM UserServer')

        for result in cur:
            username = result['UserName']
            userpassword = result['UserPassword']
            create_form_delete_user = str('net user ' + username + ' /delete')
            delete_user = subprocess.Popen(['powershell', create_form_delete_user])
            print("Пользователь: ", username, " Пароль: ", userpassword, " удален")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Osnova = QtWidgets.QWidget()
    # Установка иконки
    icon = QtGui.QIcon("kot.ico")
    Osnova.setWindowIcon(icon)
    ui = Ui_Osnova()
    ui.setupUi(Osnova)
    Osnova.show()
    sys.exit(app.exec())