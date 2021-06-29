import mysql.connector as msq


class DatabaseConnections:

    @staticmethod
    def get_connection():
        try:
            conn = msq.connect(
                host="localhost",
                user="root",
                password="24@mysqldatabase",
                database="librarydatabase")
        except msq.errors.InterfaceError as e:
            print('cannot connect to the database')
            return None, None
        curs = conn.cursor()
        return conn, curs


