from unittest import TestCase, main, mock

from internal_api import InternalAPI


class InternalAPITests(TestCase):

    def test_clean_user_input_some_cleaning(self):
        self.internal_api = InternalAPI()
        user_input = {
            'author': 'Roald Dahl',
            'categories': 'Animals, Bugs & Pets',
            'book_type': '',
            'lexile_min': '',
            'lexile_max': '',
            'book_num': 5
        }
        expected = {
            'author': 'Roald Dahl',
            'categories': 'Animals, Bugs & Pets',
            'book_num': 5
        }
        result = self.internal_api.clean_user_input(user_input)
        self.assertEqual(expected, result)

    def test_clean_user_input_nothing_to_clean(self):
        self.internal_api = InternalAPI()
        user_input = {
            'author': 'Roald Dahl',
            'categories': 'Animals, Bugs & Pets',
            'book_type': 'Fiction',
            'lexile_min': 1000,
            'lexile_max': 2000,
            'book_num': 5
        }
        expected = {
            'author': 'Roald Dahl',
            'categories': 'Animals, Bugs & Pets',
            'book_type': 'Fiction',
            'lexile_min': 1000,
            'lexile_max': 2000,
            'book_num': 5
        }
        result = self.internal_api.clean_user_input(user_input)
        self.assertEqual(expected, result)

    def test_search_book_suggestion_if_API_returns_book_on_to_read_list(self):
        pass

    def test_search_book_suggestion_if_API_returns_book_on_read_list(self):
        pass

    def test_search_book_suggestion_returns_right_number_of_books(self):
        pass

    def test_search_book_suggestion_if_no_books_returned(self):
        pass

    def test_check_for_duplicates_from_read_list_when_no_duplicates(self):
        pass

    def test_check_for_duplicates_from_read_list_when_one_duplicate(self):
        pass

    def test_check_for_duplicates_from_read_list_when_multiple_duplicates(self):
        pass

    def test_check_for_duplicates_from_to_read_list_when_no_duplicates(self):
        pass

    def test_check_for_duplicates_from_to_read_list_when_one_duplicate(self):
        pass

    def test_check_for_duplicates_from_to_read_list_when_multiple_duplicates(self):
        pass

    def test_check_random_suggestion_in_to_read_list_to_return_false(self):
        pass

    def test_check_random_suggestion_in_to_read_list_to_return_true(self):
        pass

    def test_check_random_suggestion_in_read_list_to_return_false(self):
        pass

    def test_check_random_suggestion_in_read_list_to_return_true(self):
        pass

    def test_add_to_to_read_list_when_adding_a_book(self):
        pass

    def test_add_to_to_read_list_when_book_already_on_table(self):
        pass

    def test_add_to_read_list_when_adding_a_book(self):
        pass

    def test_add_to_read_list_when_book_already_on_table(self):
        pass

    def delete_from_to_read_list_when_book_not_on_list(self):
        pass

    def delete_from_to_read_list_when_book_is_on_list(self):
        pass

    def test_get_read_list_returns_list(self):
        pass

    def test_add_a_review_for_book_not_on_list(self):
        pass

    def test_add_a_review_for_book_on_list(self):
        pass

    def test_add_star_rating_for_book_not_on_list(self):
        pass

    def test_add_star_rating_for_book_on_list(self):
        pass




    # def test_add_to_to_read_list(self):
    #     self.internal_api = InternalAPI()
    #     to_read = {
    #         'title': 'The Great Gatsby',
    #         'author': 'F. Scott Fitzgerald',
    #         'category': 'Fiction, Non-Fiction & Poetry'
    #     }
    #     expected = 'The Great Gatsby has been added to reading list'
    #     result = self.internal_api.add_to_to_read_list(to_read)
    #     self.assertEqual(expected, result)

    # def test_search_book_suggestions(self):
    #     # Create an instance of the class being tested
    #     # and any necessary dependencies
    #
    #     self.internal_api = InternalAPI()
    #     self.book_app_api = BookAppAPI()


    # def test_add_to_to_read_list_1(self):
    #     self.internal_api = InternalAPI()
    #     to_read = {
    #         'title': 'The B.F.G',
    #         'author': 'Roald Dahl',
    #         'category': 'Fiction'
    #     }
    #     expected = 'The B.F.G has been added to reading list'
    #     result = self.internal_api.add_to_to_read_list(to_read)
    #     self.assertEqual(expected, result)






if __name__ == "__main__":
    main()
