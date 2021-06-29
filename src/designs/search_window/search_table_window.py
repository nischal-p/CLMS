import sys
from PyQt4 import QtCore, QtGui
from dao.book_dao import BookDAO
from middle_men.isbn_operations import IsbnOperations
import re

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


class SearchTableWindow(object):
    def __init__(self, form):
        form.setObjectName(_fromUtf8("form"))
        form.resize(852, 542)

        self.search_box = QtGui.QLineEdit(form)
        self.search_box.setGeometry(QtCore.QRect(10, 10, 311, 31))
        self.search_box.setObjectName(_fromUtf8("search_in_books_box"))

        self.search_groupbox = QtGui.QGroupBox(form)
        self.search_groupbox.setGeometry(QtCore.QRect(330, 10, 321, 31))
        self.search_groupbox.setStyleSheet(_fromUtf8("font: 10pt \"Times New Roman\";"))
        self.search_groupbox.setTitle(_fromUtf8(""))
        self.search_groupbox.setObjectName(_fromUtf8("search_groupbox"))

        self.default_rb = QtGui.QRadioButton(self.search_groupbox)
        self.default_rb.setGeometry(QtCore.QRect(10, 10, 41, 17))
        self.default_rb.setChecked(True)
        self.default_rb.setObjectName(_fromUtf8("default_rb"))

        self.title_rb = QtGui.QRadioButton(self.search_groupbox)
        self.title_rb.setGeometry(QtCore.QRect(50, 10, 82, 17))
        self.title_rb.setObjectName(_fromUtf8("title_rb"))

        self.author_rb = QtGui.QRadioButton(self.search_groupbox)
        self.author_rb.setGeometry(QtCore.QRect(120, 10, 82, 17))
        self.author_rb.setObjectName(_fromUtf8("author_rb"))

        self.isbn_rb = QtGui.QRadioButton(self.search_groupbox)
        self.isbn_rb.setGeometry(QtCore.QRect(180, 10, 82, 17))
        self.isbn_rb.setObjectName(_fromUtf8("isbn_rb"))

        self.publisher_rb = QtGui.QRadioButton(self.search_groupbox)
        self.publisher_rb.setGeometry(QtCore.QRect(230, 10, 82, 17))
        self.publisher_rb.setObjectName(_fromUtf8("publisher_rb"))

        # this is my own code, made msq list to iterate over the available items
        self.radio_options = [self.default_rb, self.title_rb, self.author_rb, self.isbn_rb, self.publisher_rb]

        self.search_button = QtGui.QPushButton(form)
        self.search_button.setGeometry(QtCore.QRect(660, 10, 171, 31))
        self.search_button.setObjectName(_fromUtf8("search_button"))
        self.search_button.clicked.connect(self.search_clicked)

        self.divider_line = QtGui.QFrame(form)
        self.divider_line.setGeometry(QtCore.QRect(10, 50, 831, 20))
        self.divider_line.setFrameShape(QtGui.QFrame.HLine)
        self.divider_line.setFrameShadow(QtGui.QFrame.Sunken)
        self.divider_line.setObjectName(_fromUtf8("divider_line"))

        self.book_search_table = QtGui.QTableWidget(form)
        self.book_search_table.setGeometry(QtCore.QRect(10, 70, 831, 461))
        self.book_search_table.setObjectName(_fromUtf8("book_search_table"))
        self.book_search_table.setColumnCount(7)
        self.book_search_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.book_search_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.book_search_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.book_search_table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.book_search_table.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.book_search_table.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.book_search_table.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.book_search_table.setHorizontalHeaderItem(6, item)
        self.book_search_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.book_search_table.horizontalHeader()
        self.resize_empty_search_table()

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        form.setWindowTitle(_translate("form", "Search Results", None))
        self.default_rb.setText(_translate("form", "All", None))
        self.title_rb.setText(_translate("form", "Book title", None))
        self.author_rb.setText(_translate("form", "Author", None))
        self.isbn_rb.setText(_translate("form", "ISBN", None))
        self.publisher_rb.setText(_translate("form", "Publisher", None))
        self.search_button.setText(_translate("form", "Search", None))
        item = self.book_search_table.horizontalHeaderItem(0)
        item.setText(_translate("form", "ISBN", None))
        item = self.book_search_table.horizontalHeaderItem(1)
        item.setText(_translate("form", "Title", None))
        item = self.book_search_table.horizontalHeaderItem(2)
        item.setText(_translate("form", "Author", None))
        item = self.book_search_table.horizontalHeaderItem(3)
        item.setText(_translate("form", "Publisher", None))
        item = self.book_search_table.horizontalHeaderItem(4)
        item.setText(_translate("form", "Location", None))
        item = self.book_search_table.horizontalHeaderItem(5)
        item.setText(_translate("form", "Total Copies", None))
        item = self.book_search_table.horizontalHeaderItem(6)
        item.setText(_translate("form", "Available Copies", None))

    def show_result(self, result):
        self.book_search_table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.book_search_table.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                self.book_search_table.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(cell_data)))
        self.resize_full_search_table()
        # this has to be done after adding items to the table otherwise it will resize to 0 elements

    def search_clicked(self):
        self.book_search_table.clearContents()
        # clearing the table for new value to be entered
        search_keyword, filter_keyword = self.get_keywords()
        result = []
        if filter_keyword == 'All':
            result = BookDAO.search_all_fields(search_keyword)
        elif filter_keyword == 'Book title':
            result = BookDAO.search_title(search_keyword)
        elif filter_keyword == 'Author':
            result = BookDAO.search_author(search_keyword)
        elif filter_keyword == 'Publisher':
            result = BookDAO.search_publisher(search_keyword)
        elif filter_keyword == 'ISBN':
            is_isbn, isbn = IsbnOperations.validate_isbn(search_keyword)
            if is_isbn:
                result = BookDAO.search_isbn(str(isbn))
            else:
                print('is not isbn')
                result = []
        if len(result) == 0:
                print('no records found')
                self.resize_empty_search_table()
        else:
            self.show_result(result)

    def get_keywords(self):
        search_keyword = self.search_box.text()
        search_keyword = re.sub(' +', ' ', search_keyword)  # removes duplicate spaces
        # substitutes one or more occurrence of ' ' with just one ' '
        search_keyword = search_keyword.replace(':', '')
        for radio_option in self.radio_options:
            if radio_option.isChecked():
                filter_keyword = radio_option.text()
        return search_keyword, filter_keyword

    def resize_empty_search_table(self):
        header = self.book_search_table.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.Stretch)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)
        header.setResizeMode(4, QtGui.QHeaderView.Stretch)
        header.setResizeMode(5, QtGui.QHeaderView.Stretch)
        header.setResizeMode(6, QtGui.QHeaderView.Stretch)

    def resize_full_search_table(self):
        header = self.book_search_table.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(4, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(5, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(6, QtGui.QHeaderView.ResizeToContents)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form1 = QtGui.QWidget()
    table_window1 = SearchTableWindow(form1)
    form1.show()
    sys.exit(app.exec_())

