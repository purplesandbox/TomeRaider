import unittest
from unittest.mock import patch

from src.API.API_results import BookAppAPI


class BookAppAPITest(unittest.TestCase):


# Test the make_api_request function with a valid input
    def test_make_api_request_with_valid_input(self):
        user_input = {
            'author': 'J. R. R. Tolkien',
            'lexile_min': 1100,
            'lexile_max': 2000,
            'categories': None,
            'book_num': 5
        }

        # try:
        book_finder = BookAppAPI()
        expected = 1
        response = book_finder.make_api_request(user_input)
        print(response)
        if response is None:
            print("The maximum request limit is exceeded")
        else:
            self.assertEqual(expected, response['total_results'])


# Test the make_api_request with a fake url and see if the error is caught
    def test_http_error(self):
        user_input = {
            'author': 'J. R. R. Tolkien',
            'lexile_min': 1100,
            'lexile_max': 2000,
            'categories': None,
            'book_num': 5
        }
        # Create a URL that does not exist.
        url = "https://www.this-url-does-not-exist.com/"
        # create and instance of the BookAppAPI and
        instance_of_the_class = BookAppAPI()
        instance_of_the_class.endpoint = url


        # Call the `make_api_request` method.
        instance_of_the_class.make_api_request(user_input)



# Test the make_api_request function with an input which doesn't return any results
    def test_make_api_request_with_inputs_for_nonexistant_record(self):
        user_input = {
            'author': 'J. R. R. Tolkien',
            'book_type': None,
            'lexile_min': 1500,
            'lexile_max': 2000,
            'categories': None
        }

        book_finder = BookAppAPI()
        expected = None
        books_found = book_finder.make_api_request(user_input)
        self.assertEqual(expected, books_found)




# Test get_filtered_results method with a mock input from the make_api_request method
    @patch('src.API.API_results.BookAppAPI.make_api_request')
    def test_get_filtered_results(self, mock_make_api_request):
        mock_make_api_request.return_value = {'results': [{
            'authors': ['J. R. R. Tolkien'],
            'categories': ['Fiction, Non-fiction & Poetry',
            'Science Fiction & Fantasy'],
           'summary': "Set in a time far earlier than Tolkien's master works, The Hobbit "
                      'and The Lord of the Rings, this is the epic history of the elves, '
                      "and the grand story of the creation of Tolkien's magical world. "
                      'The Lord of the Rings narrated the great events at the end of the '
                      'Third Age; but the tales of The Silmarillion are legends deriving '
                      'from a much deeper past, when Morgoth, the first Dark Lord, dwelt '
                      'in Middle-earth, and the High Elves made war upon him for the '
                      "recovery of the Silmarils. Never published in the author's "
                      'lifetime, The Silmarillion is an essential compendium for all '
                      'Tolkien fans. It will be published in five consecutive volumes, '
                      'each completely unabridged. The series contains not only the '
                      'Quenta Silmarillion, but four other short works: the Ainulindale, '
                      'Valaquenta, Akallabeth and Of the Rings of Power.',
           'title': 'The Silmarillion'}], 'total_results': 1}
        user_input = {
            'author': 'J. R. R. Tolkien',
            'book_type': None,
            'lexile_min': 1100,
            'lexile_max': 2000,
            'categories': None,
            'book_num': 5
        }

        book_finder = BookAppAPI()
        records = book_finder.get_filtered_results(user_input)

        self.assertEqual(len(records), 1)
        self.assertIn('authors', records[0])
        self.assertIn('title', records[0])
        self.assertIn('categories', records[0])
        self.assertIn('summary', records[0])

# Test get_random_results method with a mock input from the make_api_request method
    @patch('src.API.API_results.BookAppAPI.make_api_request')
    def test_get_random_result(self, mock_make_api_request):
        mock_make_api_request.return_value = {'results' :[{
            'authors': ['J. R. R. Tolkien'],
            'categories': ['Fiction, Non-fiction & Poetry', 'Science Fiction & Fantasy'],
            'summary': "Set in a time far earlier than Tolkien's master works, The Hobbit "
                        'and The Lord of the Rings, this is the epic history of the elves, '
                        "and the grand story of the creation of Tolkien's magical world. "
                        'The Lord of the Rings narrated the great events at the end of the '
                        'Third Age; but the tales of The Silmarillion are legends deriving '
                        'from a much deeper past, when Morgoth, the first Dark Lord, dwelt '
                        'in Middle-earth, and the High Elves made war upon him for the '
                        "recovery of the Silmarils. Never published in the author's "
                        'lifetime, The Silmarillion is an essential compendium for all '
                        'Tolkien fans. It will be published in five consecutive volumes, '
                        'each completely unabridged. The series contains not only the '
                        'Quenta Silmarillion, but four other short works: the Ainulindale, '
                        'Valaquenta, Akallabeth and Of the Rings of Power.',
            'title': 'The Silmarillion'}]}
        user_input = {
            'author': 'J. R. R. Tolkien',
            'book_type': None,
            'lexile_min': 1100,
            'lexile_max': 2000,
            'categories': None
        }

        book_finder = BookAppAPI()
        record = book_finder.get_random_result(user_input)

        self.assertIn('authors', record)
        self.assertIn('title', record)
        self.assertIn('categories', record)
        self.assertIn('summary', record)

if __name__ == '__main__':
    unittest.main()
