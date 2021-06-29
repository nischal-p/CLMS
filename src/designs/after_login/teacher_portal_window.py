import sys
from datetime import date, timedelta
from PyQt4 import QtCore, QtGui
import re
from designs.search_window.search_table_window import SearchTableWindow
from designs.dialog_box.common_dialog_box import CommonDialogBox
from designs.dialog_box.book_in_database_dialog import BookInDatabaseDialog
from designs.dialog_box.password_enter_dialog import MasterPasswordDialog
from dao.book_dao import BookDAO
from dao.student_dao import StudentDAO
from dao.staff_dao import StaffDAO
from dao.borrow_dao import BorrowDAO
from middle_men.isbn_operations import IsbnOperations
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


class TeacherPortalWindow:

    def __init__(self, main_window, staff_username):

        self.staff_logged_in = staff_username
        self.increase_book_no_by = 0
        self.working_book_isbn = ''
        self.working_book_title = ''
        self.extract_button_clicked_once = False

        main_window.setObjectName(_fromUtf8("main_window"))
        main_window.resize(829, 623)
        main_window.setWindowIcon(QtGui.QIcon(r'E:\lbms\project_resources\claremont_logo.jpg'))

        self.centralwidget = QtGui.QWidget(main_window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.main_tab_widget = QtGui.QTabWidget(self.centralwidget)
        self.main_tab_widget.setGeometry(QtCore.QRect(0, 0, 831, 611))
        self.main_tab_widget.setObjectName(_fromUtf8("main_tab_widget"))

        self.books_tab = QtGui.QWidget()
        self.books_tab.setObjectName(_fromUtf8("books_tab"))

        self.isbn_box = QtGui.QLineEdit(self.books_tab)
        self.isbn_box.setGeometry(QtCore.QRect(10, 30, 191, 31))
        self.isbn_box.setObjectName(_fromUtf8("isbn_box"))

        self.enter_isbn_label = QtGui.QLabel(self.books_tab)
        self.enter_isbn_label.setGeometry(QtCore.QRect(10, 10, 91, 21))
        self.enter_isbn_label.setStyleSheet(_fromUtf8("font: 8pt \"MS Shell Dlg 2\";"))
        self.enter_isbn_label.setObjectName(_fromUtf8("enter_isbn_label"))

        self.enter_title_label = QtGui.QLabel(self.books_tab)
        self.enter_title_label.setGeometry(QtCore.QRect(10, 80, 91, 21))
        self.enter_title_label.setObjectName(_fromUtf8("enter_title_label"))

        self.title_box = QtGui.QLineEdit(self.books_tab)
        self.title_box.setGeometry(QtCore.QRect(10, 100, 191, 31))
        self.title_box.setObjectName(_fromUtf8("title_box"))

        self.enter_publisher_label = QtGui.QLabel(self.books_tab)
        self.enter_publisher_label.setGeometry(QtCore.QRect(10, 150, 91, 21))
        self.enter_publisher_label.setObjectName(_fromUtf8("enter_publisher_label"))

        self.publisher_box = QtGui.QLineEdit(self.books_tab)
        self.publisher_box.setGeometry(QtCore.QRect(10, 170, 191, 31))
        self.publisher_box.setObjectName(_fromUtf8("publisher_box"))

        self.extract_data_button = QtGui.QPushButton(self.books_tab)
        self.extract_data_button.setGeometry(QtCore.QRect(220, 30, 181, 31))
        self.extract_data_button.setObjectName(_fromUtf8("extract_data_button"))
        self.extract_data_button.clicked.connect(self.book_extract_data_clicked)

        self.subtitle_box = QtGui.QLineEdit(self.books_tab)
        self.subtitle_box.setGeometry(QtCore.QRect(220, 100, 191, 31))
        self.subtitle_box.setObjectName(_fromUtf8("subtitle_box"))

        self.enter_subtitle_label = QtGui.QLabel(self.books_tab)
        self.enter_subtitle_label.setGeometry(QtCore.QRect(220, 80, 91, 21))
        self.enter_subtitle_label.setObjectName(_fromUtf8("enter_subtitle_label"))

        self.enter_location_label = QtGui.QLabel(self.books_tab)
        self.enter_location_label.setGeometry(QtCore.QRect(20, 360, 91, 21))
        self.enter_location_label.setObjectName(_fromUtf8("enter_location_label"))

        self.location_combobox = QtGui.QComboBox(self.books_tab)
        self.location_combobox.setGeometry(QtCore.QRect(20, 380, 191, 31))
        self.location_combobox.setObjectName(_fromUtf8("location_combobox"))
        self.location_combobox.addItem(_fromUtf8(""))
        self.location_combobox.addItem(_fromUtf8(""))
        self.location_combobox.addItem(_fromUtf8(""))
        self.location_combobox.addItem(_fromUtf8(""))
        self.location_combobox.addItem(_fromUtf8(""))
        self.location_combobox.addItem(_fromUtf8(""))
        self.location_combobox.addItem(_fromUtf8(""))
        self.location_combobox.addItem(_fromUtf8(""))
        self.location_combobox.addItem(_fromUtf8(""))

        self.author_box = QtGui.QLineEdit(self.books_tab)
        self.author_box.setGeometry(QtCore.QRect(10, 240, 401, 41))
        self.author_box.setObjectName(_fromUtf8("author_box"))

        self.enter_author_label = QtGui.QLabel(self.books_tab)
        self.enter_author_label.setGeometry(QtCore.QRect(10, 220, 331, 21))
        self.enter_author_label.setObjectName(_fromUtf8("enter_author_label"))

        self.enter_copies_label = QtGui.QLabel(self.books_tab)
        self.enter_copies_label.setGeometry(QtCore.QRect(230, 360, 101, 21))
        self.enter_copies_label.setObjectName(_fromUtf8("enter_copies_label"))

        self.no_of_copies_box = QtGui.QLineEdit(self.books_tab)
        self.no_of_copies_box.setGeometry(QtCore.QRect(230, 380, 181, 31))
        self.no_of_copies_box.setObjectName(_fromUtf8("no_of_copies_box"))

        self.publisher_info1 = QtGui.QLabel(self.books_tab)
        self.publisher_info1.setGeometry(QtCore.QRect(220, 170, 181, 21))
        self.publisher_info1.setObjectName(_fromUtf8("publisher_info1"))

        self.publisher_info2 = QtGui.QLabel(self.books_tab)
        self.publisher_info2.setGeometry(QtCore.QRect(220, 186, 91, 16))
        self.publisher_info2.setObjectName(_fromUtf8("publisher_info2"))

        self.author_info = QtGui.QLabel(self.books_tab)
        self.author_info.setGeometry(QtCore.QRect(10, 290, 391, 16))
        self.author_info.setObjectName(_fromUtf8("author_info"))

        self.line = QtGui.QFrame(self.books_tab)
        self.line.setGeometry(QtCore.QRect(10, 320, 401, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))

        self.insert_book_button = QtGui.QPushButton(self.books_tab)
        self.insert_book_button.setGeometry(QtCore.QRect(20, 450, 391, 41))
        self.insert_book_button.setObjectName(_fromUtf8("insert_book_button"))
        self.insert_book_button.clicked.connect(self.book_insert_clicked)

        self.cancel_book_insert_button = QtGui.QPushButton(self.books_tab)
        self.cancel_book_insert_button.setGeometry(QtCore.QRect(20, 500, 391, 41))
        self.cancel_book_insert_button.setObjectName(_fromUtf8("cancel_book_insert_button"))
        self.cancel_book_insert_button.clicked.connect(self.cancel_book_insert_clicked)

        self.line_4 = QtGui.QFrame(self.books_tab)
        self.line_4.setGeometry(QtCore.QRect(430, 20, 16, 551))
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))

        self.search_groupbox = QtGui.QGroupBox(self.books_tab)
        self.search_groupbox.setGeometry(QtCore.QRect(450, 290, 351, 31))
        self.search_groupbox.setStyleSheet(_fromUtf8("font: 10pt \"Times New Roman\";"))
        self.search_groupbox.setTitle(_fromUtf8(""))
        self.search_groupbox.setObjectName(_fromUtf8("search_groupbox"))

        self.default_rb = QtGui.QRadioButton(self.search_groupbox)
        self.default_rb.setGeometry(QtCore.QRect(10, 10, 82, 17))
        self.default_rb.setChecked(True)
        self.default_rb.setObjectName(_fromUtf8("default_rb"))

        self.title_rb = QtGui.QRadioButton(self.search_groupbox)
        self.title_rb.setGeometry(QtCore.QRect(60, 10, 82, 17))
        self.title_rb.setObjectName(_fromUtf8("title_rb"))

        self.author_rb = QtGui.QRadioButton(self.search_groupbox)
        self.author_rb.setGeometry(QtCore.QRect(140, 10, 82, 17))
        self.author_rb.setObjectName(_fromUtf8("author_rb"))

        self.isbn_rb = QtGui.QRadioButton(self.search_groupbox)
        self.isbn_rb.setGeometry(QtCore.QRect(210, 10, 82, 17))
        self.isbn_rb.setObjectName(_fromUtf8("isbn_rb"))

        self.publication_rb = QtGui.QRadioButton(self.search_groupbox)
        self.publication_rb.setGeometry(QtCore.QRect(270, 10, 82, 17))
        self.publication_rb.setObjectName(_fromUtf8("publication_rb"))

        self.books_radio_options = [self.default_rb, self.isbn_rb, self.title_rb, self.author_rb, self.publication_rb]

        self.search_in_books_box = QtGui.QLineEdit(self.books_tab)
        self.search_in_books_box.setGeometry(QtCore.QRect(450, 240, 351, 41))
        self.search_in_books_box.setObjectName(_fromUtf8("search_in_books_box"))

        self.search_in_books_button = QtGui.QPushButton(self.books_tab)
        self.search_in_books_button.setGeometry(QtCore.QRect(520, 350, 211, 41))
        self.search_in_books_button.setObjectName(_fromUtf8("search_in_books_button"))
        self.search_in_books_button.clicked.connect(self.search_in_books_clicked)

        self.search_in_books_label = QtGui.QLabel(self.books_tab)
        self.search_in_books_label.setGeometry(QtCore.QRect(460, 190, 321, 51))
        self.search_in_books_label.setStyleSheet(_fromUtf8("font: 75 14pt \"Times New Roman\";"))
        self.search_in_books_label.setAlignment(QtCore.Qt.AlignCenter)
        self.search_in_books_label.setObjectName(_fromUtf8("search_in_books_label"))

        self.book_search_tip1_label = QtGui.QLabel(self.books_tab)
        self.book_search_tip1_label.setGeometry(QtCore.QRect(480, 420, 301, 31))
        self.book_search_tip1_label.setObjectName(_fromUtf8("book_search_tip1_label"))

        self.book_search_tip2_label = QtGui.QLabel(self.books_tab)
        self.book_search_tip2_label.setGeometry(QtCore.QRect(530, 440, 161, 20))
        self.book_search_tip2_label.setObjectName(_fromUtf8("book_search_tip2_label"))

        self.main_tab_widget.addTab(self.books_tab, _fromUtf8(""))
        self.students_tab = QtGui.QWidget()
        self.students_tab.setObjectName(_fromUtf8("students_tab"))

        self.std_fname_label = QtGui.QLabel(self.students_tab)
        self.std_fname_label.setGeometry(QtCore.QRect(10, 10, 91, 21))
        self.std_fname_label.setObjectName(_fromUtf8("std_fname_label"))

        self.std_fname_box = QtGui.QLineEdit(self.students_tab)
        self.std_fname_box.setGeometry(QtCore.QRect(10, 30, 241, 31))
        self.std_fname_box.setObjectName(_fromUtf8("std_fname_box"))

        self.std_lname_label = QtGui.QLabel(self.students_tab)
        self.std_lname_label.setGeometry(QtCore.QRect(10, 80, 91, 21))
        self.std_lname_label.setObjectName(_fromUtf8("std_lname_label"))

        self.std_lname_box = QtGui.QLineEdit(self.students_tab)
        self.std_lname_box.setGeometry(QtCore.QRect(10, 100, 241, 31))
        self.std_lname_box.setObjectName(_fromUtf8("std_lname_box"))

        self.std_email_label = QtGui.QLabel(self.students_tab)
        self.std_email_label.setGeometry(QtCore.QRect(10, 150, 161, 21))
        self.std_email_label.setObjectName(_fromUtf8("std_email_label"))

        self.std_email_box = QtGui.QLineEdit(self.students_tab)
        self.std_email_box.setGeometry(QtCore.QRect(10, 170, 151, 31))
        self.std_email_box.setObjectName(_fromUtf8("std_email_box"))

        self.std_fixed_email_label = QtGui.QLabel(self.students_tab)
        self.std_fixed_email_label.setGeometry(QtCore.QRect(160, 180, 151, 16))
        self.std_fixed_email_label.setStyleSheet(_fromUtf8("font: 8pt \"MS Shell Dlg 2\";"))
        self.std_fixed_email_label.setObjectName(_fromUtf8("std_fixed_email_label"))

        self.ygroup_combobox = QtGui.QComboBox(self.students_tab)
        self.ygroup_combobox.setGeometry(QtCore.QRect(10, 240, 151, 31))
        self.ygroup_combobox.setObjectName(_fromUtf8("ygroup_combobox"))
        self.ygroup_combobox.addItem(_fromUtf8(""))
        self.ygroup_combobox.addItem(_fromUtf8(""))
        self.ygroup_combobox.addItem(_fromUtf8(""))
        self.ygroup_combobox.addItem(_fromUtf8(""))
        self.ygroup_combobox.addItem(_fromUtf8(""))

        self.ygroup_label = QtGui.QLabel(self.students_tab)
        self.ygroup_label.setGeometry(QtCore.QRect(10, 220, 91, 21))
        self.ygroup_label.setObjectName(_fromUtf8("ygroup_label"))

        self.students_table = QtGui.QTableWidget(self.students_tab)
        self.students_table.setGeometry(QtCore.QRect(310, 30, 491, 371))
        self.students_table.setColumnCount(4)
        self.students_table.setObjectName(_fromUtf8("students_table"))
        self.students_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.students_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.students_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.students_table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.students_table.setHorizontalHeaderItem(3, item)
        self.students_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.insert_student_button = QtGui.QPushButton(self.students_tab)
        self.insert_student_button.setGeometry(QtCore.QRect(10, 350, 241, 41))
        self.insert_student_button.setObjectName(_fromUtf8("insert_student_button"))
        self.insert_student_button.clicked.connect(self.student_insert_clicked)

        self.line_2 = QtGui.QFrame(self.students_tab)
        self.line_2.setGeometry(QtCore.QRect(10, 310, 241, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))

        self.main_tab_widget.addTab(self.students_tab, _fromUtf8(""))
        self.staff_tab = QtGui.QWidget()
        self.staff_tab.setObjectName(_fromUtf8("staff_tab"))

        self.stf_lname_box = QtGui.QLineEdit(self.staff_tab)
        self.stf_lname_box.setGeometry(QtCore.QRect(10, 100, 211, 31))
        self.stf_lname_box.setObjectName(_fromUtf8("stf_lname_box"))

        self.stf_fname_box = QtGui.QLineEdit(self.staff_tab)
        self.stf_fname_box.setGeometry(QtCore.QRect(10, 30, 211, 31))
        self.stf_fname_box.setObjectName(_fromUtf8("stf_fname_box"))

        self.stf_fname_label = QtGui.QLabel(self.staff_tab)
        self.stf_fname_label.setGeometry(QtCore.QRect(10, 10, 91, 21))
        self.stf_fname_label.setObjectName(_fromUtf8("stf_fname_label"))

        self.stf_email_label = QtGui.QLabel(self.staff_tab)
        self.stf_email_label.setGeometry(QtCore.QRect(10, 150, 161, 21))
        self.stf_email_label.setObjectName(_fromUtf8("stf_email_label"))

        self.stf_email_box = QtGui.QLineEdit(self.staff_tab)
        self.stf_email_box.setGeometry(QtCore.QRect(10, 170, 151, 31))
        self.stf_email_box.setObjectName(_fromUtf8("stf_email_box"))

        self.stf_fixed_email_label = QtGui.QLabel(self.staff_tab)
        self.stf_fixed_email_label.setGeometry(QtCore.QRect(160, 180, 151, 16))
        self.stf_fixed_email_label.setStyleSheet(_fromUtf8("font: 8pt \"MS Shell Dlg 2\";"))
        self.stf_fixed_email_label.setObjectName(_fromUtf8("stf_fixed_email_label"))

        self.staff_table = QtGui.QTableWidget(self.staff_tab)
        self.staff_table.setGeometry(QtCore.QRect(330, 30, 461, 371))
        self.staff_table.setObjectName(_fromUtf8("staff_table"))
        self.staff_table.setColumnCount(3)
        self.staff_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.staff_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.staff_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.staff_table.setHorizontalHeaderItem(2, item)
        self.staff_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.stf_lname_label = QtGui.QLabel(self.staff_tab)
        self.stf_lname_label.setGeometry(QtCore.QRect(10, 80, 91, 21))
        self.stf_lname_label.setObjectName(_fromUtf8("stf_lname_label"))

        self.stf_password_box = QtGui.QLineEdit(self.staff_tab)
        self.stf_password_box.setGeometry(QtCore.QRect(10, 240, 211, 31))
        self.stf_password_box.setObjectName(_fromUtf8("stf_password_box"))
        self.stf_password_box.setEchoMode(QtGui.QLineEdit.Password)

        self.stf_password_label = QtGui.QLabel(self.staff_tab)
        self.stf_password_label.setGeometry(QtCore.QRect(10, 220, 91, 21))
        self.stf_password_label.setObjectName(_fromUtf8("stf_password_label"))

        self.stf_confirm_password_box = QtGui.QLineEdit(self.staff_tab)
        self.stf_confirm_password_box.setGeometry(QtCore.QRect(10, 310, 211, 31))
        self.stf_confirm_password_box.setObjectName(_fromUtf8("stf_confirm_password_box"))
        self.stf_confirm_password_box.setEchoMode(QtGui.QLineEdit.Password)

        self.stf_confirm_password_label = QtGui.QLabel(self.staff_tab)
        self.stf_confirm_password_label.setGeometry(QtCore.QRect(10, 290, 91, 21))
        self.stf_confirm_password_label.setObjectName(_fromUtf8("stf_confirm_password_label"))

        self.insert_staff_button = QtGui.QPushButton(self.staff_tab)
        self.insert_staff_button.setGeometry(QtCore.QRect(10, 370, 211, 41))
        self.insert_staff_button.setObjectName(_fromUtf8("insert_staff_button"))
        self.insert_staff_button.clicked.connect(self.staff_insert_clicked)

        self.main_tab_widget.addTab(self.staff_tab, _fromUtf8(""))
        self.borrow_tab = QtGui.QWidget()
        self.borrow_tab.setObjectName(_fromUtf8("borrow_tab"))

        self.borrow_isbn_label = QtGui.QLabel(self.borrow_tab)
        self.borrow_isbn_label.setGeometry(QtCore.QRect(10, 10, 151, 21))
        self.borrow_isbn_label.setObjectName(_fromUtf8("borrow_isbn_label"))

        self.borrow_isbn_box = QtGui.QLineEdit(self.borrow_tab)
        self.borrow_isbn_box.setGeometry(QtCore.QRect(10, 30, 191, 31))
        self.borrow_isbn_box.setObjectName(_fromUtf8("borrow_isbn_box"))

        self.borrow_username_box = QtGui.QLineEdit(self.borrow_tab)
        self.borrow_username_box.setGeometry(QtCore.QRect(220, 30, 191, 31))
        self.borrow_username_box.setObjectName(_fromUtf8("borrow_username_box"))

        self.borrow_username_label = QtGui.QLabel(self.borrow_tab)
        self.borrow_username_label.setGeometry(QtCore.QRect(220, 10, 131, 21))
        self.borrow_username_label.setObjectName(_fromUtf8("borrow_username_label"))

        self.borrow_duration_combobox = QtGui.QComboBox(self.borrow_tab)
        self.borrow_duration_combobox.setGeometry(QtCore.QRect(430, 30, 191, 31))
        self.borrow_duration_combobox.setObjectName(_fromUtf8("borrow_duration_combobox"))
        self.borrow_duration_combobox.addItem(_fromUtf8(""))
        self.borrow_duration_combobox.addItem(_fromUtf8(""))
        self.borrow_duration_combobox.addItem(_fromUtf8(""))
        self.borrow_duration_combobox.addItem(_fromUtf8(""))
        self.borrow_duration_combobox.addItem(_fromUtf8(""))

        self.borrow_duration_label = QtGui.QLabel(self.borrow_tab)
        self.borrow_duration_label.setGeometry(QtCore.QRect(430, 10, 91, 21))
        self.borrow_duration_label.setObjectName(_fromUtf8("borrow_duration_label"))

        self.lend_book_button = QtGui.QPushButton(self.borrow_tab)
        self.lend_book_button.setGeometry(QtCore.QRect(640, 30, 171, 31))
        self.lend_book_button.setObjectName(_fromUtf8("lend_book_button"))
        self.lend_book_button.clicked.connect(self.lend_book_clicked)

        self.borrows_table = QtGui.QTableWidget(self.borrow_tab)
        self.borrows_table.setGeometry(QtCore.QRect(20, 120, 781, 351))
        self.borrows_table.setObjectName(_fromUtf8("borrows_table"))
        self.borrows_table.setColumnCount(9)
        borrows_table_headers = ['Borrow ID', 'Book', 'Borrowed By', 'Issuing Staff', 'Borrow Date',
                                 'Due Date', 'Status', 'Returned Date', 'Validating Staff']
        self.borrows_table.setHorizontalHeaderLabels(borrows_table_headers)
        self.borrows_table.verticalHeader().hide()
        # the above statement would hide the automatic record numbering for the displayed borrows_table
        # so that the numbers do not visually contrast with the borrow_id numbers that would be shown right
        # beside the numberings as the first column
        self.borrows_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.borrow_table_label = QtGui.QLabel(self.borrow_tab)
        self.borrow_table_label.setGeometry(QtCore.QRect(20, 90, 421, 21))
        self.borrow_table_label.setObjectName(_fromUtf8("borrow_table_label"))

        self.send_reminders_button = QtGui.QPushButton(self.borrow_tab)
        self.send_reminders_button.setGeometry(QtCore.QRect(600, 510, 201, 41))
        self.send_reminders_button.setObjectName(_fromUtf8("send_reminders_button"))
        self.send_reminders_button.clicked.connect(self.send_reminders_clicked)

        self.line_3 = QtGui.QFrame(self.borrow_tab)
        self.line_3.setGeometry(QtCore.QRect(10, 70, 801, 20))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))

        self.search_in_borrows_box = QtGui.QLineEdit(self.borrow_tab)
        self.search_in_borrows_box.setGeometry(QtCore.QRect(490, 90, 231, 20))
        self.search_in_borrows_box.setObjectName(_fromUtf8("search_in_borrows_box"))

        self.search_in_borrows_button = QtGui.QPushButton(self.borrow_tab)
        self.search_in_borrows_button.setGeometry(QtCore.QRect(730, 90, 71, 23))
        self.search_in_borrows_button.setObjectName(_fromUtf8("search_in_borrows_button"))
        self.search_in_borrows_button.clicked.connect(self.search_in_borrows_clicked)

        self.alter_borrow_record_groupbox = QtGui.QGroupBox(self.borrow_tab)
        self.alter_borrow_record_groupbox.setGeometry(QtCore.QRect(40, 490, 371, 81))
        self.alter_borrow_record_groupbox.setObjectName(_fromUtf8("alter_borrow_record_groupbox"))

        self.borrow_id_box = QtGui.QLineEdit(self.alter_borrow_record_groupbox)
        self.borrow_id_box.setGeometry(QtCore.QRect(10, 30, 141, 31))
        self.borrow_id_box.setObjectName(_fromUtf8("borrow_id_box"))

        self.return_book_button = QtGui.QPushButton(self.alter_borrow_record_groupbox)
        self.return_book_button.setGeometry(QtCore.QRect(170, 20, 181, 41))
        self.return_book_button.setObjectName(_fromUtf8("return_book_button"))
        self.return_book_button.clicked.connect(self.return_book_clicked)

        self.reminder_date_header_label = QtGui.QLabel(self.borrow_tab)
        self.reminder_date_header_label.setGeometry(QtCore.QRect(610, 490, 111, 16))
        self.reminder_date_header_label.setObjectName(_fromUtf8("reminder_date_header_label"))

        last_notification_date = BorrowDAO.get_last_notification_date()
        self.reminder_date_value_label = QtGui.QLabel(self.borrow_tab)
        self.reminder_date_value_label.setGeometry(QtCore.QRect(720, 490, 101, 16))
        self.reminder_date_value_label.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.reminder_date_value_label.setObjectName(_fromUtf8("reminder_date_value_label"))
        self.reminder_date_value_label.setText(str(last_notification_date))

        self.main_tab_widget.addTab(self.borrow_tab, _fromUtf8(""))
        self.reports_tab = QtGui.QWidget()
        self.reports_tab.setObjectName(_fromUtf8("reports_tab"))

        self.refresh_reports_button = QtGui.QPushButton(self.reports_tab)
        self.refresh_reports_button.setGeometry(QtCore.QRect(300, 30, 191, 41))
        self.refresh_reports_button.setObjectName(_fromUtf8("refresh_reports_button"))
        self.refresh_reports_button.clicked.connect(self.refresh_reports_clicked)

        self.line_5 = QtGui.QFrame(self.reports_tab)
        self.line_5.setGeometry(QtCore.QRect(390, 110, 16, 291))
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))

        self.book_reports_table = QtGui.QTableWidget(self.reports_tab)
        self.book_reports_table.setGeometry(QtCore.QRect(30, 140, 331, 251))
        self.book_reports_table.setObjectName(_fromUtf8("book_reports_table"))
        self.book_reports_table.setColumnCount(2)
        self.book_reports_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.book_reports_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.book_reports_table.setHorizontalHeaderItem(1, item)
        self.book_reports_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.student_reports_table = QtGui.QTableWidget(self.reports_tab)
        self.student_reports_table.setGeometry(QtCore.QRect(430, 140, 361, 251))
        self.student_reports_table.setObjectName(_fromUtf8("student_reports_table"))
        self.student_reports_table.setColumnCount(2)
        self.student_reports_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.student_reports_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.student_reports_table.setHorizontalHeaderItem(1, item)
        self.student_reports_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.book_reports_label = QtGui.QLabel(self.reports_tab)
        self.book_reports_label.setGeometry(QtCore.QRect(30, 110, 321, 21))
        self.book_reports_label.setObjectName(_fromUtf8("book_reports_label"))

        self.student_reports_label = QtGui.QLabel(self.reports_tab)
        self.student_reports_label.setGeometry(QtCore.QRect(430, 110, 321, 21))
        self.student_reports_label.setObjectName(_fromUtf8("student_reports_label"))

        self.main_tab_widget.addTab(self.reports_tab, _fromUtf8(""))
        main_window.setCentralWidget(self.centralwidget)

        self.statusbar = QtGui.QStatusBar(main_window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        self.set_default_statusbar()
        main_window.setStatusBar(self.statusbar)

        self.retranslate_ui(main_window)

        self.show_students_table()
        self.show_staff_table()
        self.show_borrows_table()
        self.refresh_reports_clicked()

        self.main_tab_widget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def set_default_working_variables(self):
        # these variables are used to communicate and pass values between the Teacher Portal Window
        # and the Book in Database Dialog Box
        self.increase_book_no_by = 0
        self.working_book_isbn = ''
        self.working_book_title = ''

    def retranslate_ui(self, main_window):
        main_window.setWindowTitle(_translate("main_window1", "Claremont LBMS - Staff Portal", None))
        self.enter_isbn_label.setText(_translate("main_window1", "ISBN*", None))
        self.enter_title_label.setText(_translate("main_window1", "Title*", None))
        self.enter_publisher_label.setText(_translate("main_window1", "Publisher", None))
        self.extract_data_button.setText(_translate("main_window1", "Extract Data", None))
        self.enter_subtitle_label.setText(_translate("main_window1", "Subtitle", None))
        self.enter_location_label.setText(_translate("main_window1", "Location*", None))
        self.location_combobox.setItemText(0, _translate("main_window1", "SF1", None))
        self.location_combobox.setItemText(1, _translate("main_window1", "SF2", None))
        self.location_combobox.setItemText(2, _translate("main_window1", "SF3", None))
        self.location_combobox.setItemText(3, _translate("main_window1", "SF4", None))
        self.location_combobox.setItemText(4, _translate("main_window1", "SF5", None))
        self.location_combobox.setItemText(5, _translate("main_window1", "work room", None))
        self.location_combobox.setItemText(6, _translate("main_window1", "E1", None))
        self.location_combobox.setItemText(7, _translate("main_window1", "E2", None))
        self.location_combobox.setItemText(8, _translate("main_window1", "E3", None))
        self.enter_author_label.setText(
            _translate("main_window1", "Authors (if multiple authors, seperate author names with commas )", None))
        self.enter_copies_label.setText(_translate("main_window1", "Number of Copies*", None))
        self.publisher_info1.setText(_translate("MainWindow", "*If publisher not known, please write ", None))
        self.publisher_info2.setText(_translate("MainWindow", "\'unknown\'.", None))
        self.author_info.setText(_translate("MainWindow", "*If author not known, please write \'anonymous\'.", None))
        self.insert_book_button.setText(_translate("main_window1", "Insert New Book Record", None))
        self.cancel_book_insert_button.setText(_translate("MainWindow", "Cancel and Clear All", None))
        self.default_rb.setText(_translate("main_window1", "All ", None))
        self.title_rb.setText(_translate("main_window1", "Book title", None))
        self.author_rb.setText(_translate("main_window1", "Author", None))
        self.isbn_rb.setText(_translate("main_window1", "ISBN", None))
        self.publication_rb.setText(_translate("main_window1", "Publication", None))
        self.search_in_books_button.setText(_translate("main_window1", "Search", None))
        self.search_in_books_label.setText(_translate("main_window1", "Search for books in the Library", None))
        self.book_search_tip1_label.setText(
            _translate("MainWindow", "Tips: Simply press the Search button without typing anything", None))
        self.book_search_tip2_label.setText(_translate("MainWindow", "to view all the books in the library", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.books_tab),
                                        _translate("main_window1", "Books", None))
        self.std_fname_label.setText(_translate("main_window1", "First Name:", None))
        self.std_lname_label.setText(_translate("main_window1", "Last Name:", None))
        self.std_email_label.setText(_translate("main_window1", "School Email (only the first part) :", None))
        self.std_fixed_email_label.setText(_translate("main_window1", "@claremontseniorschool.co.uk", None))
        self.ygroup_combobox.setItemText(0, _translate("main_window1", "9", None))
        self.ygroup_combobox.setItemText(1, _translate("main_window1", "10", None))
        self.ygroup_combobox.setItemText(2, _translate("main_window1", "11", None))
        self.ygroup_combobox.setItemText(3, _translate("main_window1", "12", None))
        self.ygroup_combobox.setItemText(4, _translate("main_window1", "13", None))
        self.ygroup_label.setText(_translate("main_window1", "Year Group", None))
        item = self.students_table.horizontalHeaderItem(0)
        item.setText(_translate("main_window1", "Name", None))
        item = self.students_table.horizontalHeaderItem(1)
        item.setText(_translate("main_window1", "Email", None))
        item = self.students_table.horizontalHeaderItem(2)
        item.setText(_translate("main_window1", "Year Group", None))
        item = self.students_table.horizontalHeaderItem(3)
        item.setText(_translate("main_window1", "Available Borrowings", None))
        self.insert_student_button.setText(_translate("main_window1", "Add New Student Record", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.students_tab),
                                        _translate("main_window1", "Students", None))
        self.stf_fname_label.setText(_translate("main_window1", "First Name:", None))
        self.stf_email_label.setText(_translate("main_window1", "School Email (only the first part) :", None))
        self.stf_fixed_email_label.setText(_translate("main_window1", "@claremontseniorschool.co.uk", None))
        item = self.staff_table.horizontalHeaderItem(0)
        item.setText(_translate("main_window1", "Name", None))
        item = self.staff_table.horizontalHeaderItem(1)
        item.setText(_translate("main_window1", "Email", None))
        item = self.staff_table.horizontalHeaderItem(2)
        item.setText(_translate("main_window1", "Available Borrowings", None))
        self.stf_lname_label.setText(_translate("main_window1", "Last Name:", None))
        self.stf_password_label.setText(_translate("main_window1", "Password", None))
        self.stf_confirm_password_label.setText(_translate("main_window1", "Confirm Password:", None))
        self.insert_staff_button.setText(_translate("main_window1", "Add New Staff Record", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.staff_tab),
                                        _translate("main_window1", "Staff", None))
        self.borrow_isbn_label.setText(_translate("main_window1", "ISBN of book being borrowed:", None))
        self.borrow_username_label.setText(_translate("main_window1", "Username of staff/student:", None))
        self.borrow_duration_combobox.setItemText(0, _translate("main_window1", "1 week", None))
        self.borrow_duration_combobox.setItemText(1, _translate("main_window1", "2 weeks", None))
        self.borrow_duration_combobox.setItemText(2, _translate("main_window1", "3 weeks", None))
        self.borrow_duration_combobox.setItemText(3, _translate("main_window1", "4 weeks", None))
        self.borrow_duration_combobox.setItemText(4, _translate("main_window1", "1 day", None))
        self.borrow_duration_label.setText(_translate("main_window1", "Duration", None))
        self.lend_book_button.setText(_translate("main_window1", "Lend Book", None))
        self.borrow_table_label.setText(_translate("main_window1",
                                                   "Select a record directly or search for a book using it\'s book title or borrower\'s name/username:",
                                                   None))
        self.send_reminders_button.setText(_translate("main_window1", "Send Reminders", None))
        self.search_in_borrows_button.setText(_translate("main_window1", "Search", None))
        self.alter_borrow_record_groupbox.setTitle(_translate("MainWindow", "Enter borrowID:", None))
        self.return_book_button.setText(_translate("MainWindow", "Return the book in this record", None))
        self.reminder_date_header_label.setText(_translate("main_window1", "Last Reminder Date: ", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.borrow_tab),
                                        _translate("main_window1", "Book Borrowings and Returns", None))
        self.refresh_reports_button.setText(_translate("main_window1", "Refresh Reports", None))
        item = self.book_reports_table.horizontalHeaderItem(0)
        item.setText(_translate("main_window1", "Book Name", None))
        item = self.book_reports_table.horizontalHeaderItem(1)
        item.setText(_translate("main_window1", "Borrowed times", None))
        item = self.student_reports_table.horizontalHeaderItem(0)
        item.setText(_translate("main_window1", "Student Name", None))
        item = self.student_reports_table.horizontalHeaderItem(1)
        item.setText(_translate("main_window1", "Number of books borrowed", None))
        self.book_reports_label.setText(_translate("main_window1", "Books borrowed the highest number of times by students:", None))
        self.student_reports_label.setText(
            _translate("main_window1", "Students borrowing/reading the highest number of books: ", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.reports_tab),
                                        _translate("main_window1", "Reports", None))

    def show_students_table(self):
        result = StudentDAO.get_all_student_records()
        self.students_table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.students_table.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                self.students_table.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(cell_data)))
        header = self.students_table.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)
        # this has to be done after adding items to the table otherwise it will resize to 0 elements

    def show_staff_table(self):
        result = StaffDAO.get_all_staff_records()
        self.staff_table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.staff_table.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                self.staff_table.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(cell_data)))
        header = self.staff_table.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        # this has to be done after adding items to the table otherwise it will resize to 0 elements

    def search_in_books_clicked(self):
        search_keyword = self.search_in_books_box.text()
        for i in self.books_radio_options:
            if i.isChecked():
                filter_keyword = i.text()

        # opening the search window
        self.form1 = QtGui.QWidget()
        self.search_table_window1 = SearchTableWindow(self.form1)

        # transporting the search keyword to the search window:
        self.search_table_window1.search_box.setText(search_keyword)

        # transporting the checked filter option to the search window
        if filter_keyword == 'All':
            self.search_table_window1.default_rb.setChecked(True)
        elif filter_keyword == 'Book Title':
            self.search_table_window1.title_rb.setChecked(True)
        elif filter_keyword == 'ISBN':
            self.search_table_window1.isbn_rb.setChecked(True)
        elif filter_keyword == 'Publisher':
            self.search_table_window1.publisher_rb.setChecked(True)
        elif filter_keyword == 'Author':
            self.search_table_window1.author_rb.setChecked(True)
        self.search_table_window1.search_clicked()
        self.form1.show()

    def book_extract_data_clicked(self):
        self.statusbar.showMessage('Extracting metadata...')
        isbn1 = self.isbn_box.text()
        is_isbn, isbn1 = IsbnOperations.validate_isbn(isbn1)

        if is_isbn:
            self.extract_button_clicked_once = True
            book_details = BookDAO.check_book_in_database(isbn1)
            if book_details is not None:  # if book is already in database:
                book_title = book_details[0]
                self.working_book_title = book_title
                self.working_book_isbn = isbn1
                self.set_default_statusbar()
                self.show_book_in_database_dialog()
            else:  # if book not in database:
                metadata_exists = IsbnOperations.check_metadata(isbn1)
                print('what is returned', metadata_exists)
                if metadata_exists:
                    print('what goes in:', metadata_exists)
                    self.set_default_statusbar()
                    self.show_information_dialog('Metadata found. \nPlease enter further details and press insert '
                                                 'to add book. \nPress cancel to stop the process.')
                    book_details = IsbnOperations.get_metadata(isbn1)
                    book_details['isbn'] = isbn1

                    self.isbn_box.setText(book_details['isbn'])
                    self.title_box.setText(book_details['title'])
                    self.subtitle_box.setText(book_details['subtitle'])
                    self.publisher_box.setText(book_details['publisher'])
                    self.author_box.setText(', '.join(book_details['authors']))
                    self.isbn_box.setEnabled(False)
                else:
                    self.show_information_dialog('ISBN data for the book could not be found. ' 
                                                 'Please manually enter all relevant values.')
                    self.set_default_statusbar()
                    self.isbn_box.setEnabled(False)
        else:
            self.show_information_dialog('The entered value is not an ISBN. '
                                         'Please enter a valid ISBN')
            self.set_default_statusbar()

    def book_insert_clicked(self):
        isbn = self.isbn_box.text()
        title = self.title_box.text()
        subtitle = self.subtitle_box.text()
        publisher = self.publisher_box.text()
        location = self.location_combobox.currentText()

        unclean_input = (isbn, title, publisher)
        cleaned_input = self.clean_string_input(unclean_input)
        if cleaned_input is None:
            self.show_information_dialog('Please enter all required details.')
            return
        isbn, title, publisher = cleaned_input

        if not self.extract_button_clicked_once:
            self.show_information_dialog('Please try to extract data for the isbn once.')
            return

        authors_txt = self.author_box.text()
        authors_txt = re.sub(', +', ',', authors_txt)  # 'sue walton,    nancy andy' to 'sue walton, nancy andy
        authors_txt = re.sub(',+', ',', authors_txt)  # 'sue walton,,,,,,nancy andy' to 'sue walton,nancy andy'
        authors = authors_txt.split(',')  # 'sue walton,nancy andy' to ['sue walton', nancy andy']

        # to clean individual names as the individual author names might have duplicate spaces and more
        authors = self.clean_string_input(authors)
        if authors is None:
            self.show_information_dialog("Please enter author name. \n"
                                         "If the book has no author, enter 'Anonymous'.")

        total_copies = self.no_of_copies_box.text()
        try:
            total_copies = int(total_copies)
            if total_copies <= 0:
                raise ValueError
        except ValueError:
            # this will include: no inputs, negative  number inputs, random char inputs, decimal number inputs
            self.show_information_dialog('Please enter a valid positive integer for number of book copies.')
            return
        available_copies = total_copies

        BookDAO.insert_book(isbn, title, subtitle, authors, publisher, location, total_copies, available_copies)
        self.show_information_dialog('Book inserted!')
        self.cancel_book_insert_clicked()

    def cancel_book_insert_clicked(self):
        self.isbn_box.clear()
        self.title_box.clear()
        self.subtitle_box.clear()
        self.publisher_box.clear()
        self.author_box.clear()
        self.no_of_copies_box.clear()
        self.set_default_working_variables()
        self.set_default_statusbar()
        self.isbn_box.setEnabled(True)
        self.extract_button_clicked_once = False

    def student_insert_clicked(self):
        fname = self.std_fname_box.text()
        surname = self.std_lname_box.text()
        email = self.std_email_box.text()

        # as we are only storing the username (the first part of the email)
        email = email.replace('@claremontseniorschool.co.uk', '')

        # if the email has a server domain name other than 'claremontseniorschool.co.ik' like '@gmail.com'
        if '@' in email:
            self.show_information_dialog('Please enter a valid school email address.')
            return

        ygroup = self.ygroup_combobox.currentText()
        unclean_strings = [fname, surname, email]
        student_details = self.clean_string_input(unclean_strings)

        if student_details is None:  # if one of the details is missing
            self.show_information_dialog('Please enter all required details first.')
            return
        else:
            student_details.append(ygroup)
            result = StudentDAO.insert_student(student_details)
            if result != 'done':
                self.show_information_dialog('Student with that email (' + result + ') is already in the database.')
            else:
                self.show_students_table()
                self.show_information_dialog('Student record inserted in the database.')
            self.std_fname_box.clear()
            self.std_lname_box.clear()
            self.std_email_box.clear()

    def staff_insert_clicked(self):
        fname = self.stf_fname_box.text()
        surname = self.stf_lname_box.text()
        email = self.stf_email_box.text()
        email = email.replace('@claremontseniorschool.co.uk', '')
        if '@' in email:
            self.show_information_dialog('Please enter a valid school email address.')
            return
        password1 = self.stf_password_box.text()
        password2 = self.stf_confirm_password_box.text()
        if password1 != password2:
            self.show_information_dialog('The passwords do not match. Please try again')
            return
        if len(password1) < 8:
            self.show_information_dialog('Please enter a password with at least 8 characters.')
            return
        hashed_password = PasswordOperations.get_hashed_password_po(password1)
        unclean_strings = [fname, surname, email]
        staff_details = self.clean_string_input(unclean_strings)
        if staff_details is None:
            self.show_information_dialog('Please enter all required details first.')
            return
        else:
            staff_details.append(hashed_password)
            result = StaffDAO.insert_staff(staff_details)
            if result != 'done':
                self.show_information_dialog('Staff record for ' + result + ' is already in the database.')
            else:
                self.show_staff_table()
                self.show_information_dialog('Staff record inserted in the database.')
            self.stf_fname_box.clear()
            self.stf_lname_box.clear()
            self.stf_email_box.clear()
            self.stf_password_box.clear()
            self.stf_confirm_password_box.clear()

    def show_information_dialog(self, information_text):
        self.info_dialog = QtGui.QDialog()
        self.info_dialog_ui = CommonDialogBox(self.info_dialog, information_text)
        self.info_dialog.show()

    def show_book_in_database_dialog(self):
        self.book_in_database_dialog = QtGui.QDialog()
        self.book_in_database_dialog_ui = BookInDatabaseDialog(self.book_in_database_dialog)
        self.book_in_database_dialog.show()

        self.book_in_database_dialog_ui.ok_button.clicked.connect(self.get_number_of_copies)
        self.book_in_database_dialog_ui.cancel_button.clicked.connect(self.get_number_of_copies)

    def get_number_of_copies(self):
        self.increase_book_no_by = self.book_in_database_dialog_ui.number_of_copies
        if self.increase_book_no_by == 0:
            self.book_in_database_dialog.close()
            self.show_information_dialog('Number of book copies not increased.')
            # if cancel is pressed or 0 is entered
        elif self.increase_book_no_by < 0:
            self.show_information_dialog('Invalid Input.\nPlease enter a positive integer.')
            # for all other invalid char input
        else:
            BookDAO.increase_book_copies(self.working_book_isbn, self.increase_book_no_by)
            self.show_information_dialog('Number of copies for ' + self.working_book_title + ' increased by ' + str(self.increase_book_no_by))
            self.book_in_database_dialog.close()
        self.set_default_working_variables()
        self.cancel_book_insert_clicked()

    def lend_book_clicked(self):
        book_id = self.borrow_isbn_box.text()
        borrower_email = self.borrow_username_box.text()

        issuing_staff_email = self.staff_logged_in
        issuing_staff_id = StaffDAO.check_staff_in_database(issuing_staff_email)[0]

        book_details = BookDAO.check_book_in_database(book_id)
        if book_details is None:
            self.show_information_dialog('The entered ISBN is not in the database.\n'
                                         'Please use the search feature to copy and '
                                         'paste the ISBN of the book to be borrowed.')
            return
        book_title, available_copies = book_details

        if available_copies == 0:
            self.show_information_dialog('All copies of ' + book_title + ' have been lent out.\n'
                                         'No copies left in the library.')
            return

        student_details = StudentDAO.check_student_in_database(borrower_email)
        staff_details = StaffDAO.check_staff_in_database(borrower_email)
        if student_details is not None:
            borrower_status = 'student'
            borrower_id = student_details[0]
            borrower_name = student_details[1]
            available_borrowings = student_details[2]
        elif staff_details is not None:
            borrower_status = 'staff'
            borrower_id = staff_details[0]
            borrower_name = staff_details[1]
            available_borrowings = staff_details[2]
        else:
            self.show_information_dialog('The entered user/username could not be found in the database.\n'
                                         'Please check and try again.')
            return

        if available_borrowings == 0:
            self.show_information_dialog(borrower_name + ' has already used all of their available borrowings.\n'
                                         'Please return a borrowed book, and then try to borrow a new book.')
            self.borrow_isbn_box.clear()
            self.borrow_username_box.clear()
            return

        duration_dict = {'1 week': 7, '2 weeks': 14, '3 weeks': 21, '4 weeks': 28, '1 day': 1}
        duration_text = self.borrow_duration_combobox.currentText()
        duration = duration_dict[duration_text]

        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=duration)

        BorrowDAO.lend_book(book_id, borrower_id, borrower_status, issuing_staff_id, borrow_date, due_date)
        self.show_borrows_table()
        self.show_students_table()
        self.show_staff_table()
        self.borrow_isbn_box.clear()
        self.borrow_username_box.clear()
        self.show_information_dialog(book_title + ' lent out to ' + borrower_name)

    def return_book_clicked(self):
        borrow_id = self.borrow_id_box.text()
        borrow_status = BorrowDAO.check_borrow_record_exists(borrow_id)
        if borrow_status is None:
            self.show_information_dialog('Record does not exist for the entered borrow ID.\n'
                                         'Please enter a valid borrow ID')
            return
        elif borrow_status == 'returned':
            self.show_information_dialog("This book has already been returned")
            self.borrow_id_box.clear()
            return
        elif borrow_status == 'lost':
            self.show_information_dialog('This book has been lost and hence cannot be returned')
            self.borrow_id_box.clear()
            return

        validating_staff = StaffDAO.check_staff_in_database(self.staff_logged_in)[0]
        return_date = date.today()

        BorrowDAO.return_book(borrow_id, validating_staff, return_date)

        self.show_information_dialog('Book returned to the library')
        self.borrow_id_box.clear()
        self.show_students_table()
        self.show_staff_table()
        self.show_borrows_table()

    def search_in_borrows_clicked(self):
        search_keyword = self.search_in_borrows_box.text()
        result = BorrowDAO.search_borrows_table(search_keyword)
        self.show_borrows_table(result)

    def show_borrows_table(self, result='default'):
        if result == 'default':
            result = BorrowDAO.get_all_records()
            # the reason why I can't put BorrowDAO.get_all_records() right in the parameter default
            # value is because compile garne belama tyo value rakhera constant list of tuples banaidincha
            # so jati ota record add garepani BorrowDAO.get_all_records() ko value constant nai huncha runtime ma
            # much like how range() returns a iterable and does the range of the range() does not change
            # through out the execution of the for-range statement
        self.borrows_table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.borrows_table.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                self.borrows_table.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(cell_data)))
        self.borrows_table.resizeColumnsToContents()

    def send_reminders_clicked(self):
        last_notification_date = BorrowDAO.get_last_notification_date()
        present_date = date.today()
        if present_date > last_notification_date:
            self.master_password_dialog = QtGui.QDialog()
            self.master_password_dialog_ui = MasterPasswordDialog(self.master_password_dialog)
            self.master_password_dialog_ui.update_borrows_tab_button.clicked.connect(self.update_borrows_tab)
            self.master_password_dialog.show()
        else:
            self.show_information_dialog('Reminders for today have already been sent! Thank You!')
        self.update_borrows_tab()

    def update_borrows_tab(self):
        updated_last_notification_date = BorrowDAO.get_last_notification_date()
        self.reminder_date_value_label.setText(str(updated_last_notification_date))
        self.show_borrows_table()

    def set_default_statusbar(self):
        self.statusbar.showMessage('Logged in as: ' + self.staff_logged_in)

    def clean_string_input(self, strings):
        # cleans the arguments and returns them; returns none if one of the arguments is empty
        clean_strings = []
        for i in strings:
            if len(i) == 0:
                return None
            re.sub(' +', ' ', i)  # replaces multiple white spaces with one
            if i[0] == ' ':  # removes the first white space (if it's there)
                i[0] = ''
            if len(i) == 0:
                # this applies to both no inputs and empty white space inputs (as we removed all empty spaces above)
                return None
            clean_strings.append(i)
        return clean_strings

    def refresh_reports_clicked(self):
        student_reports = BorrowDAO.get_student_reports()
        self.student_reports_table.setRowCount(0)
        for row_number, row_data in enumerate(student_reports):
            self.student_reports_table.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                self.student_reports_table.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(cell_data)))
        self.student_reports_table.resizeColumnsToContents()

        book_reports = BorrowDAO.get_book_reports()
        self.book_reports_table.setRowCount(0)
        for row_number, row_data in enumerate(book_reports):
            self.book_reports_table.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                self.book_reports_table.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(cell_data)))
        self.book_reports_table.resizeColumnsToContents()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main_window2 = QtGui.QMainWindow()
    window1 = TeacherPortalWindow(main_window2, 'nischal.poudel')
    main_window2.show()
    sys.exit(app.exec_())
