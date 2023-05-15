class UserInteractions:
    def __init__(self):
        pass

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
                self.filtered_choice()
                break
            elif lowercase_choice == 'random':class UserInteractions:
    def __init__(self):
        pass

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
                self.filtered_choice()
                break
            elif lowercase_choice == 'random':
                self.random_choice()
                break
            elif lowercase_choice == 'to-read':
                self.view_to_read_list()
                break
            elif lowercase_choice == 'read':
                self.view_read_list()
                break
            elif lowercase_choice == 'exit':
                print('Goodbye!')
                break
            else:
                print('Invalid choice. Please try again.')

    def filtered_choice(self):

        while True:
            try:
                number_of_books = int(input('How many books would you like to search for? (Enter a number between 1 '
                                            'and 10) '))
                if number_of_books < 1 or number_of_books > 10:
                    raise ValueError('Invalid input. Please enter a number between 1 and 10.')
                break
            except ValueError as e:
                print(str(e))
                continue

        book_criteria = {
            'authors': '',
            'categories': '',
            'book_type': '',
            'lexile_min': '',
            'lexile_max': '',
            'book_num': number_of_books,
            'random_choice': False,
            'filtered_choice': True
        }
        print('What would you like to search by? (Press enter if you would like to leave blank):')
        author = input('Author: ')
        genre = input('Genre: ')
        fiction = input('Fiction or Non-Fiction: ')
        lexile_min = input('Lexile min: ')
        lexile_max = input('Lexile max: ')

        book_criteria['authors'] = author
        book_criteria['categories'] = genre
        book_criteria['book_type'] = fiction
        book_criteria['lexile_min'] = lexile_min
        book_criteria['lexile_max'] = lexile_max

        print(book_criteria)
        """Nothing is returned if I used 'return' instead of printing"""

    def random_choice(self):
        chosen_genre = input('What genre are you looking for? ')

        book_criteria = {
            'authors': '',
            'categories': chosen_genre,
            'book_type': '',
            'lexile_min': '',
            'lexile_max': '',
            'book_num': '',
            'random_choice': True,
            'filtered_choice': False
        }
        print(book_criteria)

    def add_book_to_list_or_not(self):
        while True:
            add_to_list_or_not = input('Would you like to add this book to a list? (y/n): ')
            if add_to_list_or_not.lower() == 'y':
                return True
            elif add_to_list_or_not.lower() == 'n':
                return False
            else:
                print('Invalid choice. Please try again.')

    def star_rating(self):
        user_rating = input('How many stars would you like to rate this book? (Enter a number between 1 and 5)')
        return int(user_rating)

    def view_to_read_list(self):
        return True

    def view_read_list(self):
        return True

    def regenerate_results(self):
        while True:
            happy_with_results = input('Would you like to generate different books? (y/n)')
            if happy_with_results.lower() == 'y':
                return True
            elif happy_with_results.lower() == 'n':
                return False
            else:
                print('Invalid choice. Please try again.')


user1 = UserInteractions()
user1.welcome()
                self.random_choice()
                break
            elif lowercase_choice == 'to-read':
                self.view_to_read_list()
                break
            elif lowercase_choice == 'read':
                self.view_read_list()
                break
            elif lowercase_choice == 'exit':
                print('Goodbye!')
                break
            else:
                print('Invalid choice. Please try again.')

    def filtered_choice(self):

        while True:
            try:
                number_of_books = int(input('How many books would you like to search for? (Enter a number between 1 '
                                            'and 10) '))
                if number_of_books < 1 or number_of_books > 10:
                    raise ValueError('Invalid input. Please enter a number between 1 and 10.')
                break
            except ValueError as e:
                print(str(e))
                continue

        book_criteria = {
            'authors': '',
            'categories': '',
            'book_type': '',
            'lexile_min': '',
            'lexile_max': '',
            'book_num': number_of_books,
            'random_choice': False,
            'filtered_choice': True
        }
        print('What would you like to search by? (Press enter if you would like to leave blank):')
        author = input('Author: ')
        genre = input('Genre: ')
        fiction = input('Fiction or Non-Fiction: ')
        lexile_min = input('Lexile min: ')
        lexile_max = input('Lexile max: ')

        book_criteria['authors'] = author
        book_criteria['categories'] = genre
        book_criteria['book_type'] = fiction
        book_criteria['lexile_min'] = lexile_min
        book_criteria['lexile_max'] = lexile_max

        print(book_criteria)
        """Nothing is returned if I used 'return' instead of printing"""

    def random_choice(self):
        chosen_genre = input('What genre are you looking for? ')

        book_criteria = {
            'authors': '',
            'categories': chosen_genre,
            'book_type': '',
            'lexile_min': '',
            'lexile_max': '',
            'book_num': '',
            'random_choice': True,
            'filtered_choice': False
        }
        print(book_criteria)

    def add_book_to_list_or_not(self):
        while True:
            add_to_list_or_not = input('Would you like to add this book to a list? (y/n): ')
            if add_to_list_or_not.lower() == 'y':
                return True
            elif add_to_list_or_not.lower() == 'n':
                return False
            else:
                print('Invalid choice. Please try again.')

    def star_rating(self):
        user_rating = input('How many stars would you like to rate this book? (Enter a number between 1 and 5)')
        return int(user_rating)

    def view_to_read_list(self):
        return True

    def view_read_list(self):
        return True

    def regenerate_results(self):
        while True:
            happy_with_results = input('Would you like to generate different books? (y/n)')
            if happy_with_results.lower() == 'y':
                return True
            elif happy_with_results.lower() == 'n':
                return False
            else:
                print('Invalid choice. Please try again.')


user1 = UserInteractions()
user1.welcome()

# class UserInteractions:
#     def __init__(self, search_for_book):
#         self.search_for_book = search_for_book
#
#
#
#     def welcome(self):
#         while True:
#             user_choice = input("""Welcome to {APP NAME}!\nWhat would you like to do?
#             If you would like to search for a book, enter 'search'.
#             If you would like to generate a random book, enter 'random'.
#             If you would like to look at your to-read list, enter 'to-read'.
#             If you would like to look at your read list, enter 'read'.
#             To exit the program, enter 'exit'.\nPlease enter: """)
#             lowercase_choice = user_choice.lower()
#             if lowercase_choice == 'search':
#                 self.search_for_book()
#             elif lowercase_choice == 'random':
#                 self.generate_random_book()
#             elif lowercase_choice == 'to-read':
#                 self.view_to_read_list()
#             elif lowercase_choice == 'read':
#                 self.view_read_list()
#             elif lowercase_choice == 'exit':
#                 print('Goodbye!')
#                 break
#             else:
#                 print('Invalid choice. Please try again.')
#
#         def search_for_book(self):
#             book_criteria = {}
#
#             while True:
#                 try:
#                     number_of_books = int(
#                         input('How many books would you like to search for? (Enter a number between 1 and 10) '))
#                     if number_of_books < 1 or number_of_books > 10:
#                         raise ValueError('Invalid input. Please enter a number between 1 and 10.')
#                     break
#                 except ValueError as e:
#                     print(str(e))
#                     continue
#
#             print('Enter your search parameters (leave blank for any):')
#             author = input('Author: ')
#             genre = input('Genre: ')
#             fiction = input('Fiction or Non-Fiction: ')
#             min_age = input('Minimum Age: ')
#
#             book_criteria['number_of_books'] = number_of_books
#             book_criteria['author'] = author
#             book_criteria['genre'] = genre
#             book_criteria['fiction'] = fiction
#             book_criteria['min_age'] = min_age
#
#             return book_criteria
#
#
# user1 = UserInteractions()
# user1.search_for_book()
