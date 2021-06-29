from dao.database_connector import DatabaseConnections
from middle_men.password_operations import PasswordOperations


class StaffDAO:

    @staticmethod
    def insert_staff(staff_details):
        # staff_details = (forename, surname, email, password)
        # hyaa chai password is a byte string
        conn, curs = DatabaseConnections.get_connection()
        email = staff_details[2]
        check_staff_query = '''SELECT CONCAT(forename, ' ', surname)
                                 FROM staff 
                                 WHERE email = %s
                                '''
        curs.execute(check_staff_query, (email,))
        result = curs.fetchall()
        if len(result) != 0:
            return result[0][0]
        insert_staff_query = '''INSERT INTO staff (forename, surname, email, password)
                                  VALUES (%s, %s, %s, %s)'''
        curs.execute(insert_staff_query, staff_details)
        conn.commit()
        conn.close()
        return 'done'

    @staticmethod
    def get_hashed_password_db(input_email):
        conn, curs = DatabaseConnections.get_connection()
        get_password_query = ('''SELECT password
                                FROM staff
                                WHERE email = %s''')
        curs.execute(get_password_query, (input_email,))
        result = curs.fetchall()
        if len(result) == 1:
            return result[0][0]
        return None

    @staticmethod
    def get_all_staff_records():
        conn, curs = DatabaseConnections.get_connection()
        show_all_staff_query = ('''
            SELECT CONCAT(forename, ' ', surname),
                   email,
                   available_borrowings
            FROM staff''')
        curs.execute(show_all_staff_query)
        result = curs.fetchall()
        conn.close()
        return result

    @staticmethod
    def check_staff_in_database(staff_email):
        conn, curs = DatabaseConnections.get_connection()
        check_staff_query = '''SELECT staff_id, CONCAT(forename, ' ', surname), available_borrowings
                                     FROM staff
                                     WHERE email = %s'''
        curs.execute(check_staff_query, (staff_email,))
        result = curs.fetchall()
        if len(result) == 0:
            staff_details = None
        else:
            staff_details = result[0]
        conn.close()
        return staff_details
