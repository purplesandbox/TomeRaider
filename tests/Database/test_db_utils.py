import unittest
from src.Database.db_utils import get_all_books, insert_book, move_book, delete_book, update_review, update_rating

""""
Make sure your db is empty before running these tests
"""""


class TestToReadBooksDb(unittest.TestCase):
    """
    Unit tests for testing the responsiveness of the database when working on the to_read_books table
    """
    def test_get_all_to_read_books(self):
        result = get_all_books("to_read_books")
        self.assertEqual([], result)

    def test_insert_to_read_book(self):
        inserted_book_to_read = [('The Great Gatsby', 'F.Scott Fitzgerald', 'Literary Fiction')]
        insert_book('to_read_books', 'The Great Gatsby', 'F.Scott Fitzgerald', 'Literary Fiction')
        result = get_all_books("to_read_books")
        self.assertEqual(inserted_book_to_read, result)

    def test_move_book(self):
        insert_book('to_read_books', 'Python Tricks', 'Dab Bader', 'Science & Technology')
        move_book('Python Tricks')
        result_move = get_all_books('read_books')
        self.assertEqual(result_move[0][0], 'Python Tricks')

    def test_delete_to_read_book(self):
        delete_book('to_read_books', 'The Great Gatsby')
        result = get_all_books("to_read_books")
        self.assertEqual([], result)


class TestReadBooksDb(unittest.TestCase):
    """
    Unit tests for testing the responsiveness of the database when working on the read_books table

    """
    def test_get_all_read_books(self):
        result = get_all_books("read_books")
        self.assertEqual([], result)

    def test_insert_read_book(self):
        read_book_to_insert = ('The Great Gatsby', 'F.Scott Fitzgerald', 'Literary Fiction', None, None)
        insert_book('read_books', 'The Great Gatsby', 'F.Scott Fitzgerald', 'Literary Fiction')
        result = get_all_books("read_books")
        self.assertEqual([read_book_to_insert], result)

    def test_delete_read_book(self):
        delete_book('read_books', 'The Great Gatsby')
        result = get_all_books("read_books")
        self.assertEqual([], result)

    def test_update_review(self):
        update_review('The Great Gatsby', "A great classic that I love")
        result_review = get_all_books('read_books')[-1][-2]
        self.assertEqual(result_review, "A great classic that I love")

    def test_update_rating(self):
        update_rating('The Great Gatsby', 5)
        result_rating = get_all_books('read_books')[-1][-1]
        self.assertEqual(result_rating, '5')


if __name__ == "__main__":
    unittest.main()

