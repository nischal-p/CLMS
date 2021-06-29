import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dao.borrow_dao import BorrowDAO


def send_reminder(password, book_recipient_list):
    # order:
    # start conn, ehlo, start tls, log in, make message object, send it, close connection

    try:
        conn = smtplib.SMTP('smtp.gmail.com', 587)  # email server and the port, initialise a connection with the server
    except Exception:
        # not the best idea but smtplib raises a whole lot of exceptions that cannot be caught by the try-except clause

        return 'no connection'

    sender_email = 'nischal.poudel@claremontseniorschool.co.uk'
    conn.ehlo()  # identify ourselves to the server, saying hi
    conn.starttls()  # initializes a secure connection with the server

    try:
        conn.login(sender_email, password)
    except smtplib.SMTPAuthenticationError:  #raised when the password is wrong
        conn.close()
        return 'wrong password'

    for borrow_id, recipient_email, recipient_name, book_title, due_date in book_recipient_list:
        full_recipient_email = recipient_email + '@claremontseniorschool.co.uk'
        cc = 'rpl.psycho@gmail.com'
        full_recipient_list = [full_recipient_email, cc]

        borrowing_late_for_days = get_borrowing_late_for_days(due_date)

        if borrowing_late_for_days > 15:
            cc = 'rpl.psycho@gmail.com'
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = full_recipient_email
            msg['Cc'] = cc
            msg['Subject'] = 'Book Borrowing Flagged Lost'
            due_date = str(due_date)

            body = ('Dear {0},\n\n'
                    'You have failed to return the book "{1}" by the due date ({2}). '
                    'It has been 15 days or more since the due date. So, as per the library policy, the book is '
                    'now considered lost, and you will be able to borrow one less book than you previously could.\n\n'
                    'If you can still return the book in a suitable condition, you may not be fined. '
                    'But that is a decision held by the staff overlooking the library finance '
                    'from the school finance department.\n\n'
                    'Regards,\n'
                    'Claremont Library Management').format(recipient_name, book_title, due_date)

            msg.attach(MIMEText(body, 'plain'))
            # attaching body with the rest of the email object, plain as it's plain text rather than html or xml
            final_email = msg.as_string()
            conn.sendmail(sender_email, [full_recipient_email, cc], final_email)

            BorrowDAO.set_flag_lost(borrow_id)
        else:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = full_recipient_email
            msg['Subject'] = 'Book Borrowing Crossed Due Date'

            body = ('Dear {0},\n\n'
                    'Your book borrowing for "{1}" has crossed its due date ({2}). Please return the book promptly.\n\n'
                    'Regards,\n'
                    'Claremont Library Management').format(recipient_name, book_title, due_date)

            msg.attach(MIMEText(body, 'plain'))
            # attaching body with the rest of the email object, plain as it's plain text rather than html or xml
            text = msg.as_string()
            conn.sendmail(sender_email, full_recipient_email, text)

    conn.close()  # close the parameters
    return 'done'


def get_borrowing_late_for_days(due_date):
    present_date = date.today()
    result = (present_date - due_date).days
    return result



