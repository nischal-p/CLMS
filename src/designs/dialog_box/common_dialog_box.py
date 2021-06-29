import sys
from PyQt4 import QtCore, QtGui

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


class CommonDialogBox:

    def __init__(self, dialog, dialog_text):

        self.this_dialog = dialog
        self.this_dialog.setObjectName(_fromUtf8("dialog1"))
        self.this_dialog.resize(391, 181)

        self.dialog_text_box = QtGui.QTextBrowser(self.this_dialog)
        self.dialog_text_box.setGeometry(QtCore.QRect(10, 10, 371, 121))
        self.dialog_text_box.setObjectName(_fromUtf8("dialog_text_box"))
        self.dialog_text_box.setText(dialog_text)

        self.ok_button = QtGui.QPushButton(self.this_dialog)
        self.ok_button.setGeometry(QtCore.QRect(130, 140, 131, 31))
        self.ok_button.setObjectName(_fromUtf8("ok_button"))
        self.ok_button.clicked.connect(self.ok_clicked)

        self.retranslateUi(self.this_dialog)
        QtCore.QMetaObject.connectSlotsByName(self.this_dialog)

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(_translate("dialog1", "Information", None))
        self.ok_button.setText(_translate("dialog1", "OK", None))

    def ok_clicked(self):
        self.this_dialog.close()


if __name__ == "__main__":
    dtext = '''This is an information box. The information is shown here like this. Press OK to close this box.'''
    app = QtGui.QApplication(sys.argv)
    dialog1 = QtGui.QDialog()
    ui = CommonDialogBox(dialog1, dtext)
    dialog1.show()
    sys.exit(app.exec_())

