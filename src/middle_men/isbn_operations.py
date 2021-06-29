import urllib.request
import json
import isbnlib


# the order in which book_details is being read;
# isbn, title, subtitle, authors, publisher, location, total_copies, available_copies

class IsbnOperations:

    # checks if input is isbn, and returns isbn 13 if entered isbn is isbn 10
    @staticmethod
    def validate_isbn(isbn):
        isbn = isbnlib.clean(isbn)  # this will remove any white spaces or other unnecessary chars and return msq str isbn
        if len(isbn) == 13:
            if isbnlib.is_isbn13(isbn):
                return True, isbn
            else:
                return False, -1
        elif len(isbn) == 10:
            if isbnlib.is_isbn10(isbn):
                isbn = isbnlib.to_isbn13(isbn)
                return True, isbn
            else:
                return False, -1
        else:
            return False, -1
        # returning the isbn too to change isbn 10 to isbn 13

    # this to get the metadata from the google api
    @staticmethod
    def get_metadata(isbn):
        query = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'
        while True:
            try:
                x = urllib.request.urlopen(query + isbn)  # opens the mentioned url and returns HTTP response object
                x = x.read().decode(
                    'utf-8')  # changes the byte response to readable byte and then to string
                metadata = json.loads(x)
                break
            except urllib.error.URLError:  # raised if no internet connection
                return None

        full_book_details = metadata['items'][0]['volumeInfo']
        title = full_book_details['title']
        try:
            subtitle = full_book_details['subtitle']
        except KeyError:  # raised if book has no subtitle
            subtitle = ''
        try:
            authors = full_book_details['authors']
            # this authors is different as it is from the dictionary from the json api
        except KeyError:  # raised if book has no authors
            authors = []
        try:
            publisher = full_book_details['publisher']
        except KeyError:  # raised if book has no publisher
            publisher = ''
        specific_book_details = {'title': title, 'subtitle': subtitle, 'publisher': publisher, 'authors': authors}
        return specific_book_details

    # checks if there is any data to be extracted
    @staticmethod
    def check_metadata(isbn):
        try:
            metadata = isbnlib.meta(isbn, service='goob')
            # this will only change the google book api as that's where we are extracting data from
            '''it will return none: 1)if there is no data to be found, or 
               2)if there is no internet connection'''
        except Exception:
            print('we got here')
            return False
        print('for some reason, we also got here')
        return True



