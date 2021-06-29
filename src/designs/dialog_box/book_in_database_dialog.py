import sys
from PyQt4 import QtCore, QtGui
from designs.dialog_box.common_dialog_box import CommonDialogBox

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


class BookInDatabaseDialog:

    def __init__(self, dialog):

        self.this_dialog = dialog
        self.this_dialog.setObjectName(_fromUtf8("dialog1"))
        self.this_dialog.resize(390, 177)

        self.information_text = QtGui.QTextBrowser(self.this_dialog)
        self.information_text.setGeometry(QtCore.QRect(20, 10, 351, 91))
        self.information_text.setObjectName(_fromUtf8("information_text"))

        self.number_of_copies_label = QtGui.QLabel(self.this_dialog)
        self.number_of_copies_label.setGeometry(QtCore.QRect(50, 130, 91, 20))
        self.number_of_copies_label.setObjectName(_fromUtf8("number_of_copies_label"))

        self.number_of_copies_box = QtGui.QLineEdit(self.this_dialog)
        self.number_of_copies_box.setGeometry(QtCore.QRect(150, 130, 41, 31))
        self.number_of_copies_box.setObjectName(_fromUtf8("number_of_copies_box"))

        self.number_of_copies = 0

        self.ok_button = QtGui.QPushButton(self.this_dialog)
        self.ok_button.setGeometry(QtCore.QRect(220, 130, 75, 23))
        self.ok_button.setObjectName(_fromUtf8("ok_button"))
        self.ok_button.clicked.connect(self.ok_button_clicked)

        self.cancel_button = QtGui.QPushButton(self.this_dialog)
        self.cancel_button.setGeometry(QtCore.QRect(300, 130, 75, 23))
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.cancel_button.clicked.connect(self.cancel_button_clicked)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.this_dialog)

    def ok_button_clicked(self):
        number_of_copies = self.number_of_copies_box.text()
        try:
            self.number_of_copies = int(number_of_copies)
        except ValueError:
            # this will include: no inputs, negative  number inputs, random char inputs, decimal number inputs
            self.number_of_copies = -1

    def cancel_button_clicked(self):
        self.number_of_copies = 0

    def retranslate_ui(self):
        self.this_dialog.setWindowTitle(_translate("dialog1", "Book Already in Database", None))
        self.information_text.setHtml(_translate("dialog1", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This book is already in the database.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If you would like to increase the total number of copies in the database by a certain number, please enter that number and press OK. </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Otherwise, press Cancel.</p></body></html>", None))
        self.number_of_copies_label.setText(_translate("dialog1", "Number of copies:", None))
        self.ok_button.setText(_translate("dialog1", "OK", None))
        self.cancel_button.setText(_translate("dialog1", "Cancel", None))

    def show_information_dialog(self, information_text):
        self.dialog2 = QtGui.QDialog()
        self.dialog_ui = CommonDialogBox(self.dialog2, information_text)
        self.dialog2.show()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog1 = QtGui.QDialog()
    ui = BookInDatabaseDialog(dialog1)
    dialog1.show()
    sys.exit(app.exec_())

