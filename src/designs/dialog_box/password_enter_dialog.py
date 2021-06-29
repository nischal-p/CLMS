import sys
from datetime import date
from PyQt4 import QtCore, QtGui
from designs.dialog_box.common_dialog_box import CommonDialogBox
from dao.borrow_dao import BorrowDAO
from middle_men.email_operations import send_reminder

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


class MasterPasswordDialog:

    def __init__(self, dialog):

        self.this_dialog = dialog
        self.this_dialog.setObjectName(_fromUtf8("dialog1"))
        self.this_dialog.resize(417, 115)

        self.master_password_label = QtGui.QLabel(self.this_dialog)
        self.master_password_label.setGeometry(QtCore.QRect(10, 10, 171, 21))
        self.master_password_label.setObjectName(_fromUtf8("master_password_label"))

        self.master_password_box = QtGui.QLineEdit(self.this_dialog)
        self.master_password_box.setGeometry(QtCore.QRect(190, 10, 221, 31))
        self.master_password_box.setObjectName(_fromUtf8("master_password_box"))
        self.master_password_box.setEchoMode(QtGui.QLineEdit.Password)  # this masks/hides our password input

        self.send_reminders_confirmation_button = QtGui.QPushButton(self.this_dialog)
        self.send_reminders_confirmation_button.setGeometry(QtCore.QRect(210, 70, 121, 31))
        self.send_reminders_confirmation_button.setObjectName(_fromUtf8("send_reminders_confirmation_button"))
        self.send_reminders_confirmation_button.clicked.connect(self.send_reminders_confirmation_clicked)

        self.line = QtGui.QFrame(self.this_dialog)
        self.line.setGeometry(QtCore.QRect(7, 50, 401, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))

        self.cancel_button = QtGui.QPushButton(self.this_dialog)
        self.cancel_button.setGeometry(QtCore.QRect(80, 70, 121, 31))
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.cancel_button.clicked.connect(self.cancel_reminders_clicked)

        self.update_borrows_tab_button = QtGui.QPushButton(self.this_dialog)
        self.update_borrows_tab_button.setVisible(False)
        # this invisible button had to be introduced because after sending the reminders and possibly
        # flagging books as lost, the displayed borrow table did not update in the send_reminders_clicked()
        # of the teacher portal. so, this had to be done, so that once the reminders are sent, a click
        # of update_borrows_tab_button is simulated(this acts as a signal) which would then run the update_borrows_tab()
        # method of the TeacherPortal class

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.this_dialog)

    def retranslateUi(self):
        self.this_dialog.setWindowTitle(_translate("dialog1", "Enter Password", None))
        self.master_password_label.setText(_translate("dialog1", "Enter the library email password:", None))
        self.send_reminders_confirmation_button.setText(_translate("dialog1", "Send Reminders", None))
        self.cancel_button.setText(_translate("dialog1", "Cancel", None))

    def show_information_dialog(self, information_text):
        self.information_dialog = QtGui.QDialog()
        self.information_dialog_ui = CommonDialogBox(self.information_dialog, information_text)
        self.information_dialog.show()

    def send_reminders_confirmation_clicked(self):
        master_password = self.master_password_box.text()
        book_recipient_list = BorrowDAO.get_reminder_recipient_list()

        if len(book_recipient_list) == 0:
            self.show_information_dialog('No reminders to be sent; no book borrowings crossing the due date.')
            BorrowDAO.set_last_notification_date(date.today())
            # as even though we haven't sent any reminders, all necessary and relevant checks have already
            # been carried out
            self.this_dialog.close()
            return  # the method will continue to run (even after dialog is closed) unless return is called

        reminder_sent_status = send_reminder(master_password, book_recipient_list)
        if reminder_sent_status == 'no connection':
            self.show_information_dialog('No internet connection.\n'
                                         'Please try again when there is an active internet connection.')
            self.this_dialog.close()
        elif reminder_sent_status == 'wrong password':
            self.show_information_dialog('Wrong password!')
        elif reminder_sent_status == 'done':
            BorrowDAO.set_last_notification_date(date.today())
            self.update_borrows_tab_button.click()
            self.show_information_dialog('Reminders sent!')
            self.this_dialog.close()
        return

    def cancel_reminders_clicked(self):
        self.this_dialog.close()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    master_password_dialog = QtGui.QDialog()
    master_password_dialog_ui = MasterPasswordDialog(master_password_dialog)
    master_password_dialog.show()
    sys.exit(app.exec_())

