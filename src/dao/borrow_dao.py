from dao.database_connector import DatabaseConnections


class BorrowDAO:

    @staticmethod
    def lend_book(book_id, borrower_id, borrower_status, issuing_staff, borrow_date, due_date):
        conn, curs = DatabaseConnections.get_connection()
        status = 'borrowed'

        if borrower_status == 'student':
            student_id = borrower_id
            staff_id = None
            update_student_record_query = '''UPDATE students
                                             SET available_borrowings = available_borrowings - 1
                                             WHERE student_id = %s
                                             '''
            curs.execute(update_student_record_query, (student_id,))
            conn.commit()
        elif borrower_status == 'staff':
            student_id = None
            staff_id = borrower_id
            update_staff_record_query = '''UPDATE staff
                                           SET available_borrowings = available_borrowings - 1
                                           WHERE staff_id = %s
                                        '''
            curs.execute(update_staff_record_query, (staff_id,))
            conn.commit()

        insert_borrow_items = (book_id, student_id, staff_id, issuing_staff, borrow_date, due_date, status, book_id)

        insert_borrow_query = '''INSERT INTO book_borrowings 
                                (book_id, borrowing_student, borrowing_staff, issuing_staff, borrow_date, due_date, status)
                                 VALUES (%s, %s, %s, %s, %s, %s, %s);
                                 
                                 UPDATE books
                                 SET available_copies = available_copies - 1
                                 WHERE isbn = %s;'''
        for i in curs.execute(insert_borrow_query, insert_borrow_items, multi=True):
            # this is to execute multiple queries at the same time
            pass
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def return_book(borrow_id, validating_staff, returned_date):

        # extract isbn from borrow record and increase available_copies count
        # extract borrower_id and increase available_borrowings
        # change status to 'returned'

        conn, curs = DatabaseConnections.get_connection()
        return_book_query1 = '''UPDATE book_borrowings
                                SET status = 'returned', returned_date = %s, validating_staff = %s
                                WHERE borrow_id = %s;
                                
                                SELECT book_id,
                                       IF(bor.borrowing_student is NULL,
                                          bor.borrowing_staff,
                                          bor.borrowing_student) AS borrower_id,
                                       IF(bor.borrowing_student is NULL,
                                          'staff',
                                          'student') AS borrower_status
                                FROM book_borrowings AS bor
                                WHERE bor.borrow_id = %s;'''
        for i in curs.execute(return_book_query1, (returned_date, validating_staff, borrow_id, borrow_id,), multi=True):
            # this has to be done to execute multiple sql queries
            pass
        borrow_details = curs.fetchone()
        conn.commit()  # should be committed after result has been fetched
        book_id, borrower_id, borrower_status = borrow_details

        if borrower_status == 'student':
            reset_available_borrowings_query = '''
            UPDATE students 
            SET available_borrowings = available_borrowings + 1
            WHERE student_id = %s'''
        elif borrower_status == 'staff':
            reset_available_borrowings_query = '''
            UPDATE staff 
            SET available_borrowings = available_borrowings + 1
            WHERE staff_id = %s'''

        curs.execute(reset_available_borrowings_query, (borrower_id,))
        conn.commit()

        reset_available_copies_query = '''
        UPDATE books
        SET available_copies = available_copies + 1
        WHERE isbn = %s;'''
        curs.execute(reset_available_copies_query, (book_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_last_notification_date():
        conn, curs = DatabaseConnections.get_connection()
        get_date_quer = '''SELECT last_notification_date
                           FROM table_of_commons
                           WHERE id=1;'''
        curs.execute(get_date_quer)
        date = curs.fetchall()[0][0]
        conn.close()
        return date

    @staticmethod
    def set_last_notification_date(ln_date):
        conn, curs = DatabaseConnections.get_connection()
        set_ln_date_query = '''UPDATE table_of_commons
                               SET last_notification_date = %s
                               WHERE id = 1;'''
        curs.execute(set_ln_date_query, (ln_date,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_records():
        conn, curs = DatabaseConnections.get_connection()
        show_all_query = '''
        SELECT bor.borrow_id,
               IF(b.subtitle IS NULL or b.subtitle = ' ', 
                  b.title, 
                  CONCAT(b.title, ' : ', b.subtitle)) as borrowed_book,
               IF(CONCAT(br_sd.forename, ' ', br_sd.surname)IS NULL,
                  CONCAT(br_sf.forename, ' ', br_sf.surname),
                  CONCAT(br_sd.forename, ' ', br_sd.surname)) AS borrowed_by,
                  CONCAT(iss_sf.forename, ' ', iss_sf.surname) as issuing_staff,
               bor.borrow_date,
               bor.due_date,
               bor.status,
               IF(bor.returned_date IS NULL, '-', bor.returned_date),
               IF(bor.validating_staff IS NULL, '-', CONCAT(val_sf.forename, ' ', val_sf.surname))
        FROM book_borrowings AS bor
        LEFT JOIN books AS b ON bor.book_id = b.isbn
        LEFT JOIN students as br_sd on bor.borrowing_student = br_sd.student_id
        LEFT JOIN staff AS br_sf ON bor.borrowing_staff = br_sf.staff_id
        LEFT JOIN staff AS iss_sf on bor.issuing_staff = iss_sf.staff_id
        LEFT JOIN staff as val_sf on bor.validating_staff = val_sf.staff_id
        ORDER BY bor.borrow_date DESC'''
        curs.execute(show_all_query)
        result = curs.fetchall()
        conn.close()
        return result

    @staticmethod
    def search_borrows_table(search_keyword):
        conn, curs = DatabaseConnections.get_connection()
        search_query = '''
                SELECT bor.borrow_id,
                       IF(b.subtitle IS NULL or b.subtitle = ' ',
                          b.title, 
                          CONCAT(b.title, ' : ', b.subtitle)) as borrowed_book,
                       IF(CONCAT(br_sd.forename, ' ', br_sd.surname)IS NULL,
                          CONCAT(br_sf.forename, ' ', br_sf.surname),
                          CONCAT(br_sd.forename, ' ', br_sd.surname)) AS borrowed_by,
                       CONCAT(iss_sf.forename, ' ', iss_sf.surname) as issuing_staff,
                       bor.borrow_date,
                       bor.due_date,
                       bor.status,
                       IF(bor.returned_date IS NULL, '-', bor.returned_date),
                       IF(bor.validating_staff IS NULL, '-', CONCAT(val_sf.forename, ' ', val_sf.surname))
                FROM book_borrowings AS bor
                LEFT JOIN books AS b ON bor.book_id = b.isbn
                LEFT JOIN students as br_sd on bor.borrowing_student = br_sd.student_id
                LEFT JOIN staff AS br_sf ON bor.borrowing_staff = br_sf.staff_id
                LEFT JOIN staff AS iss_sf on bor.issuing_staff = iss_sf.staff_id
                LEFT JOIN staff as val_sf on bor.validating_staff = val_sf.staff_id
                WHERE CONCAT(b.title, ' ', b.subtitle) LIKE CONCAT(%s,'%') OR
                      br_sd.email = %s OR
                      CONCAT(br_sd.forename, ' ', br_sd.surname) LIKE CONCAT(%s, '%') OR
                      br_sf.email = %s OR
                      CONCAT(br_sf.forename, ' ', br_sf.surname) LIKE CONCAT(%s, '%')
                ORDER BY bor.borrow_date DESC'''
        curs.execute(search_query, (search_keyword, search_keyword, search_keyword, search_keyword, search_keyword,))
        result = curs.fetchall()
        conn.close()
        return result

    @staticmethod
    def check_borrow_record_exists(borrow_id):
        conn, curs = DatabaseConnections.get_connection()
        check_query = '''
        SELECT status 
        FROM book_borrowings 
        WHERE borrow_id = %s'''
        curs.execute(check_query, (borrow_id,))
        result = curs.fetchall()
        if len(result) == 0:
            return None
        else:
            return result[0][0]

    @staticmethod
    def get_reminder_recipient_list():
        conn, curs = DatabaseConnections.get_connection()
        get_recipient_list_query = '''
        SELECT borrow_id,
               IF(bor.borrowing_student is NULL,
                  br_stf.email,
                  br_std.email) AS borrower_email,
               IF(bor.borrowing_student IS NULL,
                  br_stf.forename,
                  br_std.forename) AS borrowed_by,
               IF(b.subtitle IS NULL or b.subtitle = ' ', 
                  b.title, 
                  CONCAT(b.title, ' : ', b.subtitle)) ,
               bor.due_date  
        FROM book_borrowings AS bor
        LEFT JOIN books AS b ON bor.book_id = b.isbn
        LEFT JOIN students AS br_std ON bor.borrowing_student = br_std.student_id
        LEFT JOIN staff AS br_stf ON bor.borrowing_staff = br_stf.staff_id
        WHERE CURRENT_DATE > bor.due_date AND
              bor.status = 'borrowed'; '''
        curs.execute(get_recipient_list_query)
        book_recipient_list = curs.fetchall()
        conn.close()
        return book_recipient_list

    @staticmethod
    def set_flag_lost(borrow_id):
        conn, curs = DatabaseConnections.get_connection()
        flag_lost_query1 = '''UPDATE book_borrowings
                              SET status = 'lost'
                              WHERE borrow_id = %s;
                              
                              SELECT book_id
                              FROM book_borrowings AS bor
                              WHERE bor.borrow_id = %s'''
        for i in curs.execute(flag_lost_query1, (borrow_id, borrow_id,), multi=True):
            pass
        book_id = curs.fetchone()[0]
        conn.commit()
        decrease_total_book_query = '''UPDATE books
                                       SET total_copies = total_copies - 1
                                       WHERE isbn = %s'''
        curs.execute(decrease_total_book_query, (book_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_student_reports():
        conn, curs = DatabaseConnections.get_connection()
        get_student_reports_query = '''
        SELECT CONCAT(br_sd.forename, ' ', br_sd.surname),
               COUNT(bor.borrowing_student) AS c
        FROM book_borrowings AS bor
        LEFT JOIN students AS br_sd ON bor.borrowing_student = br_sd.student_id
        WHERE bor.borrowing_student IS NOT NULL
        GROUP BY bor.borrowing_student DESC
        ORDER BY c DESC'''
        curs.execute(get_student_reports_query)
        result = curs.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_book_reports():
        conn, curs = DatabaseConnections.get_connection()
        get_book_reports_query = '''
        SELECT IF(b.subtitle IS NULL or b.subtitle = ' ', 
                  b.title, 
                  CONCAT(b.title, ' : ', b.subtitle)) AS book_title,
               COUNT(bor.book_id) AS no_of_times_borrowed
        FROM book_borrowings AS bor
        LEFT JOIN books AS b on bor.book_id = b.isbn
        WHERE bor.borrowing_student IS NOT NULL
        GROUP BY bor.book_id DESC
        ORDER BY no_of_times_borrowed DESC'''
        curs.execute(get_book_reports_query)
        result = curs.fetchall()
        conn.close()
        return result



