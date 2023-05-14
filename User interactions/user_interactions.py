class UserInteractions:
    def __init__(self, api, db):
        self.api = api
        self.db = db


"""function to search for book - asks user what type of book, calls API function, 
calls add to list function, calls add notes to lsit function"""

    def search_for_book(self):
        book_criteria = input('What type of book are you looking for? (customise to search params): ')
        number_of_books = int(input('How many books would you like to search for?: '))
        # save results as variable book
        # API call with book_criteria to return number_of_books books
        # Display the search results to the user
        self.add_book_or_not(book)
        self.add_notes_to_book(book)

"""function to generate random book - asks user what type of book, calls API function, 
calls add to list function, calls add notes to lsit function"""
    def generate_random_book(self):
        book_criteria = input('What type of book are you looking for? (customise to search params): ')
        number_of_books = int(input('How many books would you like to generate?: '))
        # call API function to return random book
        # Display the search results to the user
        self.add_book_or_not(book)
        self.add_notes_to_book(book)

"""add book to list or not"""
    def add_book_or_not(self, book):
        add_to_list_or_not = input('Would you like to add this book to a list? (y/n): ')
        if add_to_list_or_not == 'y':
            which_list = input('Which list would you like to add this book to? (to-read/read): ')
            if which_list == 'to-read':
                self.add_to_to_read_list(book)
            elif which_list == 'read':
                self.add_to_read_list(book)
            else:
                print('Invalid choice. Please try again.')
        elif add_to_list_or_not == 'n':
            print('Okay')
        else:
            print('Invalid choice. Please try again.')

    def add_to_to_read_list(self, book):
        pass
    """code to add book into database"""

    def add_to_read_list(self, book):
        pass
    """code to add book into database"""

    def view_to_read_list(self):
        pass

    def view_read_list(self):
        pass

"""add notes/review to book or not"""
    def add_notes_to_book(self, book):
        add_notes_or_not = input('Would you like to add notes to this book')
        if add_notes_or_not == 'y':
            add_notes = input('What notes would you like to add?: ')
            book.add_notes(add_notes)
        elif add_notes_or_not == 'n':
            print('Okay')

"""welcome function - asks user what they would like to do"""
    def welcome(self):
        while True:
            user_choice = input("""Welcome to {APP NAME}!\nWhat would you like to do?
            If you would like to search for a book, enter 'search'.
            If you would like to generate a random book, enter 'random'.
            If you would like to look at your to-read list, enter 'to-read'.
            If you would like to look at your read list, enter 'read'.
            To exit the program, enter 'exit'.\nPlease enter: """)
            lowercase_choice = user_choice.lower()
            if lowercase_choice == 'search':
                self.search_for_book()
            elif lowercase_choice == 'random':
                self.generate_random_book()
            elif lowercase_choice == 'to-read':
                self.view_to_read_list()
            elif lowercase_choice == 'read':
                self.view_read_list()
            elif lowercase_choice == 'exit':
                print('Goodbye!')
                break
            else:
                print('Invalid choice. Please try again.')


UserInteractions.welcome('hi')
