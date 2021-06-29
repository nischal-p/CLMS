from dao.database_connector import DatabaseConnections


class StudentDAO:

    @staticmethod
    def insert_student(student_details):
        # (forename, surname, email, year_group) = student_details
        conn, curs = DatabaseConnections.get_connection()
        email = student_details[2]
        check_student_query = '''SELECT CONCAT(forename, ' ', surname)
                                 FROM students 
                                 WHERE email = %s
                                 '''
        curs.execute(check_student_query, (email,))
        result = curs.fetchall()
        if len(result) != 0:
            return result[0][0]
        insert_student_query = '''INSERT INTO students (forename, surname, email, year_group)
                                  VALUES (%s, %s, %s, %s)'''
        curs.execute(insert_student_query, student_details)
        conn.commit()
        conn.close()
        return 'done'

    @staticmethod
    def get_all_student_records():
        conn, curs = DatabaseConnections.get_connection()
        show_all_students_query = ('''
        SELECT CONCAT(forename, ' ', surname),
               email,
               year_group,
               available_borrowings
        FROM students''')
        curs.execute(show_all_students_query)
        result = curs.fetchall()
        conn.close()
        return result

    @staticmethod
    def check_student_in_database(student_email):
        conn, curs = DatabaseConnections.get_connection()
        check_student_query = '''SELECT student_id, CONCAT(forename, ' ', surname), available_borrowings
                                 FROM students
                                 WHERE email = %s'''
        curs.execute(check_student_query, (student_email,))
        result = curs.fetchall()
        if len(result) == 0:
            student_details = None
        else:
            student_details = result[0]
        conn.close()
        return student_details
