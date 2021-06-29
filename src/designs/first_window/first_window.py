import sys
from PyQt4 import QtCore, QtGui
from designs.search_window.search_table_window import SearchTableWindow
from designs.after_login.teacher_portal_window import TeacherPortalWindow
from designs.dialog_box.common_dialog_box import CommonDialogBox
from dao.staff_dao import StaffDAO
from middle_men.password_operations import PasswordOperations

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class FirstWindow:
    def __init__(self, main_window):
        main_window.setObjectName(_fromUtf8("main_window1"))
        main_window.resize(740, 595)
        main_window.setWindowIcon(QtGui.QIcon(r'E:\lbms\project_resources\claremont_logo.jpg'))

        self.centralwidget = QtGui.QWidget(main_window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.search_box = QtGui.QLineEdit(self.centralwidget)
        self.search_box.setGeometry(QtCore.QRect(110, 240, 431, 41))
        self.search_box.setObjectName(_fromUtf8("search_in_books_box"))

        self.search_button = QtGui.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(570, 240, 111, 41))
        self.search_button.setObjectName(_fromUtf8("search_button"))
        self.search_button.clicked.connect(self.search_clicked)

        self.tip = QtGui.QLabel(self.centralwidget)
        self.tip.setGeometry(QtCore.QRect(170, 380, 371, 16))
        self.tip.setObjectName(_fromUtf8("tip"))

        self.header_label = QtGui.QLabel(self.centralwidget)
        self.header_label.setGeometry(QtCore.QRect(70, 170, 521, 61))
        self.header_label.setStyleSheet(_fromUtf8("font: 75 18pt \"Times New Roman\";"))
        self.header_label.setAlignment(QtCore.Qt.AlignCenter)
        self.header_label.setObjectName(_fromUtf8("header_label"))

        self.email_label = QtGui.QLabel(self.centralwidget)
        self.email_label.setGeometry(QtCore.QRect(20, 500, 131, 16))
        self.email_label.setObjectName(_fromUtf8("email_label"))

        self.password_label = QtGui.QLabel(self.centralwidget)
        self.password_label.setGeometry(QtCore.QRect(260, 500, 51, 16))
        self.password_label.setObjectName(_fromUtf8("password_label"))

        self.email_box = QtGui.QLineEdit(self.centralwidget)
        self.email_box.setGeometry(QtCore.QRect(20, 520, 221, 31))
        self.email_box.setObjectName(_fromUtf8("std_email_box"))

        self.password_box = QtGui.QLineEdit(self.centralwidget)
        self.password_box.setGeometry(QtCore.QRect(260, 520, 201, 31))
        self.password_box.setObjectName(_fromUtf8("password_box"))
        self.password_box.setEchoMode(QtGui.QLineEdit.Password)  # this masks our password/hides it from the user

        self.login_button = QtGui.QPushButton(self.centralwidget)
        self.login_button.setGeometry(QtCore.QRect(480, 520, 111, 31))
        self.login_button.setObjectName(_fromUtf8("login_button"))
        self.login_button.clicked.connect(self.login_clicked)

        self.login_label = QtGui.QLabel(self.centralwidget)
        self.login_label.setGeometry(QtCore.QRect(20, 470, 151, 21))
        self.login_label.setStyleSheet(_fromUtf8("font: 14pt \"Times New Roman\";"))
        self.login_label.setObjectName(_fromUtf8("login_label"))

        self.header2_label = QtGui.QLabel(self.centralwidget)
        self.header2_label.setGeometry(QtCore.QRect(170, 290, 311, 41))
        self.header2_label.setStyleSheet(_fromUtf8("font: 75 12pt \"Times New Roman\";"))
        self.header2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.header2_label.setObjectName(_fromUtf8("header2_label"))

        self.status_label = QtGui.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(170, 470, 281, 21))
        self.status_label.setText(_fromUtf8(""))
        self.status_label.setObjectName(_fromUtf8("status_label"))

        self.search_groupbox = QtGui.QGroupBox(self.centralwidget)
        self.search_groupbox.setGeometry(QtCore.QRect(120, 300, 491, 51))
        self.search_groupbox.setStyleSheet(_fromUtf8("font: 10pt \"Times New Roman\";"))
        self.search_groupbox.setObjectName(_fromUtf8("search_groupbox"))

        self.default_rb = QtGui.QRadioButton(self.search_groupbox)
        self.default_rb.setGeometry(QtCore.QRect(10, 30, 82, 17))
        self.default_rb.setChecked(True)
        self.default_rb.setObjectName(_fromUtf8("default_rb"))

        self.title_rb = QtGui.QRadioButton(self.search_groupbox)
        self.title_rb.setGeometry(QtCore.QRect(120, 30, 82, 17))
        self.title_rb.setObjectName(_fromUtf8("title_rb"))

        self.author_rb = QtGui.QRadioButton(self.search_groupbox)
        self.author_rb.setGeometry(QtCore.QRect(220, 30, 82, 17))
        self.author_rb.setObjectName(_fromUtf8("author_rb"))

        self.isbn_rb = QtGui.QRadioButton(self.search_groupbox)
        self.isbn_rb.setGeometry(QtCore.QRect(300, 30, 82, 17))
        self.isbn_rb.setObjectName(_fromUtf8("isbn_rb"))

        self.publisher_rb = QtGui.QRadioButton(self.search_groupbox)
        self.publisher_rb.setGeometry(QtCore.QRect(380, 30, 82, 17))
        self.publisher_rb.setObjectName(_fromUtf8("publisher_rb"))

        self.radio_options = [self.default_rb, self.title_rb, self.author_rb, self.isbn_rb, self.publisher_rb]

        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(main_window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        main_window.setStatusBar(self.statusbar)

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def search_clicked(self):
        search_keyword = self.search_box.text()
        for i in self.radio_options:
            if i.isChecked():
                filter_keyword = i.text()
        self.form1 = QtGui.QWidget()
        self.table_window1 = SearchTableWindow(self.form1)
        self.table_window1.search_box.setText(search_keyword)
        if filter_keyword == 'All':
            self.table_window1.default_rb.setChecked(True)
        elif filter_keyword == 'Book title':
            self.table_window1.title_rb.setChecked(True)
        elif filter_keyword == 'ISBN':
            self.table_window1.isbn_rb.setChecked(True)
        elif filter_keyword == 'Publisher':
            self.table_window1.publisher_rb.setChecked(True)
        elif filter_keyword == 'Author':
            self.table_window1.author_rb.setChecked(True)
        self.table_window1.search_clicked()

        self.search_box.clear()  # to clear the search box and the radio options for next search
        self.default_rb.setChecked(True)
        # here so that input extraction from these would be completed

        self.form1.show()

    def login_clicked(self):
        input_email = self.email_box.text()
        input_password = self.password_box.text()

        # to get the password value in the database in the staff record with the entered email
        password_in_database = StaffDAO.get_hashed_password_db(input_email)

        if password_in_database is not None:  # if a staff record having the entered email exists
            password_match = PasswordOperations.compare_password(input_password, password_in_database)
            if password_match:
                self.email_box.clear()
                self.password_box.clear()
                self.open_teacher_portal(input_email)
            else:
                self.status_label.setText('Login unsuccessful, please try again')
                self.show_information_dialog('Incorrect email/password. Please check both and try again.')
        else:  # if a staff record having the entered email doesn't exist
            self.status_label.setText('Login unsuccessful, please try again')
            self.show_information_dialog('Incorrect email/password. Please check both and try again.')

    def show_information_dialog(self, information_text):
        self.info_dialog = QtGui.QDialog()
        self.info_dialog_ui = CommonDialogBox(self.info_dialog, information_text)
        self.info_dialog.show()

    def open_teacher_portal(self, staff_logging_in):
        self.teacher_portal = QtGui.QMainWindow()
        self.teacher_portal_ui = TeacherPortalWindow(self.teacher_portal, staff_logging_in)
        self.teacher_portal.show()

    def retranslate_ui(self, main_window):
        main_window.setWindowTitle(_translate("main_window1", "Claremont Library Management System", None))
        self.search_button.setText(_translate("main_window1", "Search", None))
        self.header_label.setText(_translate("main_window1", "Claremont Library Management System", None))
        self.login_button.setText(_translate("main_window1", "Login", None))
        self.login_label.setText(_translate("main_window1", "Login for Staff", None))
        self.search_groupbox.setTitle(_translate("main_window1", "Search using book title, author, publisher or isbn", None))
        self.default_rb.setText(_translate("main_window1", "All", None))
        self.title_rb.setText(_translate("main_window1", "Book title", None))
        self.author_rb.setText(_translate("main_window1", "Author", None))
        self.isbn_rb.setText(_translate("main_window1", "ISBN", None))
        self.publisher_rb.setText(_translate("main_window1", "Publisher", None))
        self.email_label.setText(_translate("MainWindow", "Email (only the first part):", None))
        self.password_label.setText(_translate("MainWindow", "Password:", None))
        self.tip.setText(
            _translate("MainWindow", "Tip: to view all books in the library, simply hit search without typing anything",
                       None))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main_window1 = QtGui.QMainWindow()
    first_window1 = FirstWindow(main_window1)
    main_window1.show()
    sys.exit(app.exec_())
