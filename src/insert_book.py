from middle_men.isbn_operations import IsbnOperations
from dao.book_dao import BookDAO

# the order in which book_details is being read;
# isbn, title, subtitle, authors, publication, book_location, total_copies, available_copies

isbn1 = input('enter isbn: ')
is_isbn, isbn1 = IsbnOperations.validate_isbn(isbn1)
if is_isbn:
    book_in_database = BookDAO.check_book_in_database(isbn1)
    if book_in_database is not None:
        print('book already in database')
    else:
        is_metadata = IsbnOperations.check_metadata(isbn1)
        if is_metadata:
            book_details_dictionary = IsbnOperations.get_metadata(isbn1)
            print('metadata found, please enter further details')
            print(book_details_dictionary)

            book_details_dictionary['isbn'] = isbn1
            book_details_dictionary['location'] = input('enter book location: ')
            book_details_dictionary['total_copies'] = int(input('enter total number of copies: '))
            book_details_dictionary['available_copies'] = book_details_dictionary['total_copies']

            book_details_list = []
            list_order = ('isbn', 'title', 'subtitle', 'authors', 'publisher', 'location', 'total_copies', 'available_copies')
            for i in list_order:
                book_details_list.append(book_details_dictionary[i])
            print(book_details_list)
            BookDAO.insert_book(book_details_list)
        else:
            print('no metadata found')
else:
    print('it is not an isbn')


