from dao.database_connector import DatabaseConnections


class BookDAO:

    @staticmethod
    def insert_book(isbn, title, subtitle, authors, publisher, location, total_copies, available_copies):
        """this method assumes that it has already been established that the book
        is not already in the database"""
        insert_book_query = '''
          INSERT INTO books
          VALUES (%s, %s, %s, %s, %s, %s, %s);
        '''
        insert_book_item = (isbn, title, subtitle, publisher, location, total_copies, available_copies)
        conn, curs = DatabaseConnections.get_connection()
        curs.execute(insert_book_query, insert_book_item)
        conn.commit()

        # inserting authors of the book in the database
        for author in authors:
            author_position = authors.index(author) + 1
            author_in_database = BookDAO.get_author_id(author)
            if author_in_database is not None:  # checks if author's already in database
                author_id = author_in_database  # if yes, get the author id
            else:
                author_id = BookDAO.insert_author(author)
                # if no, insert a new record and get its author_id

            insert_books_authors_query = '''INSERT INTO books_authors (book_id, author_id, author_position)
                                            VALUES (%s, %s, %s);'''
            insert_books_authors_item = (isbn, author_id, author_position)
            curs.execute(insert_books_authors_query, insert_books_authors_item)
            conn.commit()
        conn.close()
        return 'done'

    @staticmethod
    def increase_book_copies(isbn, copies):
        conn, curs = DatabaseConnections.get_connection()
        increase_query = '''UPDATE books
                              SET total_copies = total_copies + %s, available_copies = available_copies + %s
                              WHERE isbn = %s'''
        increase_items = (copies, copies, isbn)
        curs.execute(increase_query, increase_items)
        conn.commit()
        conn.close()

    @staticmethod
    def insert_author(author):
        conn, curs = DatabaseConnections.get_connection()
        insert_author_query = '''INSERT INTO authors (forename, middle_name, surname)
                                                    VALUES (%s, %s, %s);
                                                    SELECT LAST_INSERT_ID();'''
        author_names = author.split(' ')  # splits author's name into individual forename, middle name and surname
        if len(author_names) >= 3:
            forename, middle_name, surname = author_names[0], author_names[1], author_names[-1]
        elif len(author_names) == 2:
            forename, middle_name, surname = author_names[0], '', author_names[-1]
        else:
            forename, middle_name, surname = author_names[0], '', ''
        insert_author_item = (forename, middle_name, surname)

        for i in curs.execute(insert_author_query, insert_author_item, multi=True):
            # this has to be done to execute multiple sql queries at the same time
            pass

        author_id = curs.fetchall()[0][0]  # has to be read before it is committed
        # the [0][0] index because LAST_INSERT_ID() returns a list of tuples
        conn.commit()
        conn.close()
        return author_id

    @staticmethod
    def get_author_id(author):
        conn, curs = DatabaseConnections.get_connection()
        get_author_id_query = '''SELECT author_id 
                                 FROM authors AS a
                                 WHERE IF(a.middle_name IS NULL or a.middle_name = ' ', CONCAT(a.forename, ' ', a.surname), CONCAT(a.forename, ' ', a.middle_name, ' ', a.surname)) 
                                 LIKE CONCAT(%s,'%') 
                               '''
        curs.execute(get_author_id_query, (author,))
        result = curs.fetchall()
        conn.close()
        author_id = None
        if len(result) == 1:
            author_id = result[0][0]
        return author_id

    @staticmethod
    def search_all_fields(search_keyword):
        conn, curs = DatabaseConnections.get_connection()
        search_all_query = ('''
            SELECT b.isbn,
                   IF(b.subtitle IS NULL or b.subtitle = ' ', 
                      b.title, CONCAT(b.title, ' : ', 
                      b.subtitle)) as book_title,
                   GROUP_CONCAT(IF(a.middle_name IS NULL or a.middle_name = ' ', 
                                   CONCAT(a.forename, ' ', a.surname), 
                                   CONCAT(a.forename, ' ', a.middle_name, ' ', a.surname))) as authors,
                   b.publisher,
                   b.location,
                   b.total_copies,
                   b.available_copies
            FROM books AS b
            JOIN books_authors AS ba on ba.book_id = b.isbn
            JOIN authors AS a on a.author_id = ba.author_id
            WHERE (CONCAT(b.title, ' ', b.subtitle) LIKE CONCAT(%s,'%') OR
                   b.subtitle LIKE CONCAT(%s,'%') OR
                   CONCAT(a.forename, ' ', a.middle_name, ' ', a.surname) LIKE CONCAT(%s,'%') OR
                   CONCAT(a.forename, ' ', a.surname) LIKE CONCAT(%s,'%') OR
                   CONCAT(a.middle_name, ' ', a.surname) LIKE CONCAT(%s,'%') OR
                   b.isbn = %s OR
                   b.publisher LIKE CONCAT(%s,'%'))
            GROUP BY b.isbn
            ORDER BY b.title''')
        curs.execute(search_all_query, (
        search_keyword, search_keyword, search_keyword, search_keyword, search_keyword, search_keyword,
        search_keyword,))
        result = curs.fetchall()
        conn.close()
        return result

    @staticmethod
    def search_publisher(search_keyword):
        conn, curs = DatabaseConnections.get_connection()
        search_publisher_query = ('''
        SELECT b.isbn,
               IF(b.subtitle IS NULL or b.subtitle = ' ', b.title, CONCAT(b.title, ' : ', b.subtitle)),
               GROUP_CONCAT(IF(a.middle_name IS NULL or a.middle_name = ' ', CONCAT(a.forename, ' ', a.surname), CONCAT(a.forename, ' ', a.middle_name, ' ', a.surname))),
               b.publisher,
               b.location,
               b.total_copies,
               b.available_copies
        FROM books AS b
        JOIN books_authors AS ba on ba.book_id = b.isbn
        JOIN authors AS a on a.author_id = ba.author_id
        WHERE b.publisher LIKE CONCAT(%s,'%')  
        GROUP BY b.isbn
        ORDER BY b.title''')
        curs.execute(search_publisher_query, (search_keyword,))
        result = curs.fetchall()
        conn.close()
        return result

    @staticmethod
    def search_author(search_keyword):
        conn, curs = DatabaseConnections.get_connection()
        search_author_query = ('''
        SELECT b.isbn,
               IF(b.subtitle IS NULL or b.subtitle = ' ', b.title, CONCAT(b.title, ' : ', b.subtitle)),
               GROUP_CONCAT(IF(a.middle_name IS NULL or a.middle_name = ' ', CONCAT(a.forename, ' ', a.surname), CONCAT(a.forename, ' ', a.middle_name, ' ', a.surname))),
               b.publisher,
               b.location,
               b.total_copies,
               b.available_copies
        FROM books AS b
        JOIN books_authors AS ba on ba.book_id = b.isbn
        JOIN authors AS a on a.author_id = ba.author_id
        WHERE (CONCAT(a.forename, ' ', a.middle_name, ' ', a.surname) LIKE CONCAT(%s,'%') OR
               CONCAT(a.forename, ' ', a.surname) LIKE CONCAT(%s,'%') OR
               CONCAT(a.middle_name, ' ', a.surname) LIKE CONCAT(%s,'%'))
        GROUP BY b.isbn
        ORDER BY b.title''')
        curs.execute(search_author_query, (search_keyword, search_keyword, search_keyword,))
        result = curs.fetchall()
        conn.close()
        return result

    @staticmethod
    def search_title(search_keyword):
        conn, curs = DatabaseConnections.get_connection()
        search_author_query = ('''
        SELECT b.isbn,
               IF(b.subtitle IS NULL or b.subtitle = ' ', b.title, CONCAT(b.title, ' : ', b.subtitle)),
               GROUP_CONCAT(IF(a.middle_name IS NULL or a.middle_name = ' ', CONCAT(a.forename, ' ', a.surname), CONCAT(a.forename, ' ', a.middle_name, ' ', a.surname))),
               b.publisher,
               b.location,
               b.total_copies,
               b.available_copies
        FROM books AS b
        JOIN books_authors AS ba on ba.book_id = b.isbn
        JOIN authors AS a on a.author_id = ba.author_id
        WHERE CONCAT(b.title, ' ', b.subtitle) LIKE CONCAT(%s,'%') OR
               b.subtitle LIKE CONCAT(%s,'%')
        GROUP BY b.isbn
        ORDER BY b.title''')
        # can also search just by the subtitle as that was the whole point why
        # we went through the lengthy process of extracting it
        # so i can search using all of ('alan turing', 'the enigma', and 'alan turing : the enigma')
        curs.execute(search_author_query, (search_keyword, search_keyword,))
        result = curs.fetchall()
        conn.close()
        return result

    @staticmethod
    def search_isbn(search_keyword):
        conn, curs = DatabaseConnections.get_connection()
        search_isbn_query = ('''
        SELECT b.isbn,
               IF(b.subtitle IS NULL or b.subtitle = ' ', b.title, CONCAT(b.title, ' : ', b.subtitle)),
               GROUP_CONCAT(IF(a.middle_name IS NULL or a.middle_name = ' ', CONCAT(a.forename, ' ', a.surname), CONCAT(a.forename, ' ', a.middle_name, ' ', a.surname))),
               b.publisher,
               b.location,
               b.total_copies,
               b.available_copies
        FROM books AS b
        JOIN books_authors AS ba on ba.book_id = b.isbn
        JOIN authors AS a on a.author_id = ba.author_id
        WHERE b.isbn = %s  
        GROUP BY b.isbn
        ORDER BY b.title''')
        curs.execute(search_isbn_query, (search_keyword,))
        # the query does not work without the brackets
        result = curs.fetchall()
        conn.close()
        return result

    @staticmethod
    def check_book_in_database(isbn):
        conn, curs = DatabaseConnections.get_connection()
        check_book_query = '''SELECT IF(b.subtitle IS NULL or b.subtitle = ' ', b.title, CONCAT(b.title, ' : ', b.subtitle)),
                                     b.available_copies
                              FROM books AS b
                              WHERE isbn = %s 
                           '''
        curs.execute(check_book_query, (isbn,))
        result = curs.fetchall()
        if len(result) == 1:
            book_details = result[0]
        else:
            book_details = None
        conn.close()
        return book_details







