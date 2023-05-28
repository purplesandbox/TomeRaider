import unittest
from unittest import mock
from unittest.mock import patch
from src.user_interactions.user_interactions import UserInteractions
from io import StringIO
import sys


class TestWelcome(unittest.TestCase):
    """Testing the welcome function - commented out tests take a long time to run but eventually pass"""

    def setUp(self):
        self.userinteractions = UserInteractions()

    # @patch('builtins.input', return_value='search')
    # def test_welcome_search(self, mocked_input):
    #     with patch.object(self.userinteractions, 'filtered_choice') as mock_filtered_choice:
    #         self.userinteractions.welcome()
    #         mock_filtered_choice.assert_called_once()

    # @patch('builtins.input', return_value='random')
    # def test_welcome_random(self, mocked_input):
    #     with patch.object(self.userinteractions, 'random_choice') as mock_random_choice:
    #         self.userinteractions.welcome()
    #         mock_random_choice.assert_called_once()

    # @patch('builtins.input', return_value='to-read')
    # def test_welcome_to_read(self, mocked_input):
    #     with patch.object(self.userinteractions, 'view_to_read_list') as mock_view_to_read_list:
    #         self.userinteractions.welcome()
    #         mock_view_to_read_list.assert_called_once()
    #
    # @patch('builtins.input', return_value='read')
    # def test_welcome_read(self, mocked_input):
    #     with patch.object(self.userinteractions, 'view_read_list') as mock_view_read_list:
    #         self.userinteractions.welcome()
    #         mock_view_read_list.assert_called_once()

    @patch('builtins.input', return_value='exit')
    def test_welcome_exit(self, mocked_input):
        with patch('builtins.print') as mock_print:
            self.userinteractions.welcome()
            mock_print.assert_called_once_with('Goodbye!')

    # @patch('builtins.input', return_value='add')
    # def test_welcome_add(self, mocked_input):
    #     with patch.object(self.userinteractions, 'add_book_to_read_list') as mock_add_book:
    #         self.userinteractions.welcome()
    #         mock_add_book.assert_called_once()


class TestNumberOfBooks(unittest.TestCase):
    """Test number of books function"""

    def setUp(self):
        self.userinteractions = UserInteractions()

    def test_get_number_of_books_valid_input(self):
        with patch('builtins.input', return_value='5'):
            result = self.userinteractions.get_number_of_books()
            self.assertEqual(result, 5)

    def test_get_number_of_books_invalid_input(self):
        with patch('builtins.input', side_effect=['0', '11', '6']):
            with patch('builtins.print') as mock_print:
                self.userinteractions.get_number_of_books()
                expected_error_message = 'Invalid input. Please enter a number between 1 and 10.'
                mock_print.assert_called_with(expected_error_message)

    def test_get_number_of_books_edge_case_minimum(self):
        with patch('builtins.input', return_value='1'):
            result = self.userinteractions.get_number_of_books()
            self.assertEqual(result, 1)

    def test_get_number_of_books_edge_case_maximum(self):
        with patch('builtins.input', return_value='10'):
            result = self.userinteractions.get_number_of_books()
            self.assertEqual(result, 10)


class TestPrintSearchCriteriaMessage(unittest.TestCase):
    """Test print search criteria message function"""

    def setUp(self):
        self.userinteractions = UserInteractions()

    def test_print_search_criteria_message(self):
        with patch('builtins.print') as mock_print:
            self.userinteractions.print_search_criteria_message()
            mock_print.assert_called_with(
                'What would you like to search by? (Press enter if you would like to leave blank): ')


class TestPrintBookGenreDictionary(unittest.TestCase):
    """Test print book genre dictionary function"""

    def setUp(self):
        self.userinteractions = UserInteractions()

    def test_print_book_genre_dictionary(self):
        expected_output = '''You can choose from the following categories: 
1: Animals, Bugs & Pets
2: Art, Creativity & Music
3: General Literature
4: Hobbies, Sports & Outdoors
5: Science Fiction & Fantasy
6: Real Life
7: Science & Technology
8: Mystery & Suspense
9: Reference
'''
        with patch("sys.stdout", new=StringIO()) as dictionary_message:
            self.userinteractions.print_book_genre_dictionary()
            self.assertEqual(dictionary_message.getvalue(), expected_output)


class TestGetValidGenreChoice(unittest.TestCase):
    """Tests for get_valid_genre_choice function"""

    def setUp(self):
        self.userinteractions = UserInteractions()

    def test_get_valid_genre_choice_valid_input(self):
        with patch('builtins.input', return_value='5'):
            expected = 'Science Fiction & Fantasy'
            result = self.userinteractions.get_valid_genre_choice()
            self.assertEqual(result, expected)

    def test_get_valid_genre_choice_empty_input(self):
        with patch('builtins.input', return_value=''):
            expected = None
            result = self.userinteractions.get_valid_genre_choice()
            self.assertEqual(result, expected)

    def test_get_valid_genre_choice_invalid_input(self):
        with patch('builtins.input', side_effect=['0', '']):
            expected_output = 'Invalid genre choice. Please choose a valid number from the genre choices.'
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = self.userinteractions.get_valid_genre_choice()
                self.assertEqual(result, None)  # No valid genre choice entered
                self.assertEqual(mock_stdout.getvalue().strip(), expected_output)


class TestValidateInputYorN(unittest.TestCase):
    """Tests for validate_input_y_or_n function"""

    def setUp(self):
        self.userinteractions = UserInteractions()

    def test_validate_input_y_or_n_valid_input(self):
        with patch('builtins.input', return_value='y'):
            result = self.userinteractions.validate_input_y_or_n('Prompt')
            self.assertEqual(result, 'y')

        with patch('builtins.input', return_value='n'):
            result = self.userinteractions.validate_input_y_or_n('Prompt')
            self.assertEqual(result, 'n')

    def test_validate_input_y_or_n_invalid_input_then_valid_input(self):
        with patch('builtins.input', side_effect=['invalid', 'y']):
            result = self.userinteractions.validate_input_y_or_n('Prompt')
            self.assertEqual(result, 'y')

        with patch('builtins.input', side_effect=['invalid', 'n']):
            result = self.userinteractions.validate_input_y_or_n('Prompt')
            self.assertEqual(result, 'n')

    def test_validate_input_y_or_n_case_insensitive(self):
        with patch('builtins.input', return_value='Y'):
            result = self.userinteractions.validate_input_y_or_n('Prompt')
            self.assertEqual(result, 'y')

        with patch('builtins.input', return_value='N'):
            result = self.userinteractions.validate_input_y_or_n('Prompt')
            self.assertEqual(result, 'n')


class TestValidateFictionNonFiction(unittest.TestCase):
    """Tests for validate fiction or nonfiction input"""

    def setUp(self):
        self.user_interactions = UserInteractions()

    def test_validate_fiction_nonfiction_input_valid_input(self):
        valid_inputs = ['fiction', 'nonfiction', '']
        for input_value in valid_inputs:
            with patch('builtins.input', return_value=input_value):
                result = self.user_interactions.validate_fiction_nonfiction_input()
                self.assertEqual(result, input_value)

    # This test takes a long time to run
    # def test_validate_fiction_nonfiction_input_invalid_input(self):
    #     invalid_inputs = ['orange', 'apple']
    #     for input_value in invalid_inputs:
    #         with patch('builtins.input', return_value=input_value), \
    #                 patch('builtins.print') as mock_print:
    #             result = self.user_interactions.validate_fiction_nonfiction_input()
    #             self.assertEqual(result, None)
    #             mock_print.assert_called_with(
    #                 "Invalid input. Please enter 'fiction' or 'nonfiction', or press enter if you have no preference. ")


class TestGetValidStarRating(unittest.TestCase):
    """Test get valid star rating function"""

    def setUp(self):
        self.userinteractions = UserInteractions()

    @patch('builtins.input')
    def test_get_valid_star_rating_valid_input(self, mock_input):
        mock_input.return_value = '4'

        result = self.userinteractions.get_valid_star_rating()

        self.assertEqual(result, 4)

    @patch('builtins.input')
    def test_get_valid_star_rating_invalid_input(self, mock_input):
        mock_input.side_effect = ['abc', '6', '2']
        with patch('builtins.print') as mock_print:
            result = self.userinteractions.get_valid_star_rating()
        self.assertEqual(result, 2)
        mock_print.assert_called_with("Please enter a number between 1 and 5.")

    @patch('builtins.input')
    def test_get_valid_star_rating_out_of_range_input(self, mock_input):
        mock_input.side_effect = ['0', '7', '3']
        with patch('builtins.print') as mock_print:
            result = self.userinteractions.get_valid_star_rating()
        self.assertEqual(result, 3)
        mock_print.assert_called_with("Please enter a number between 1 and 5.")


class TestUserReviewStarRating(unittest.TestCase):
    """Tests for user_review_and_call_star_rating function"""

    def setUp(self):
        self.userinteractions = UserInteractions()

    @patch('builtins.input')
    def test_user_review_and_call_star_rating_add_review(self, mock_input):
        mock_input.side_effect = ['y', 'Really nice to read.', '5']
        with patch.object(self.userinteractions.internal_api, 'add_a_review') as mock_add_review, \
                patch.object(self.userinteractions, 'star_rating') as mock_star_rating:
            read_book_dict = {'title': 'Monday Morning', 'author': 'Author', 'categories': 'Fiction'}
            self.userinteractions.user_review_and_call_star_rating(read_book_dict)
            mock_add_review.assert_called_with(read_book_dict, 'Really nice to read.')
            mock_star_rating.assert_called_with(read_book_dict)

    @patch('builtins.input')
    def test_user_review_and_call_star_rating_no_review(self, mock_input):
        mock_input.side_effect = ['n', '4']
        with patch.object(self.userinteractions, 'star_rating') as mock_star_rating:
            read_book_dict = {'title': 'Harry Potter', 'author': 'J.K. Rowling', 'categories': 'Fiction'}
            self.userinteractions.user_review_and_call_star_rating(read_book_dict)
            mock_star_rating.assert_called_with(read_book_dict)
            mock_star_rating.assert_called_with(read_book_dict)


class TestValidateLexileMinMax(unittest.TestCase):
    """Testing ValidateLexileMinMax function"""

    def setUp(self):
        self.userinteractions = UserInteractions()

    @patch('builtins.input', side_effect=['500', '1000', ''])
    def test_validate_lexile_min_and_max_input(self, mock_input):
        # Test valid input within the range
        result = self.userinteractions.validate_lexile_min_and_max_input()
        self.assertEqual(result, 500)

        result = self.userinteractions.validate_lexile_min_and_max_input()
        self.assertEqual(result, 1000)

        result = self.userinteractions.validate_lexile_min_and_max_input()
        self.assertEqual(result, '')


if __name__ == '__main__':
    unittest.main()
