from unittest import TestCase, main, mock

from src.API.internal_api import InternalAPI, BookAlreadyOnTable, BookNotFound
import responses


def mock_db_responses(read, to_read):
    return lambda input: read if input == 'read_books' else to_read if input == 'to_read_books' else []


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

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('The Witches', 'Roald Dahl', 'Science Fiction & Fantasy')
                    ]
                ))
    @responses.activate
    def test_search_book_suggestion_no_duplicates(self, mock_get_all_books):
        self.internal_api = InternalAPI()
        book_results = [
            {
                'authors': ['Roald Dahl'],
                'title': 'The Magic Finger',
                'categories': ['Hobbies, Sports & Outdoors',
                               'Fiction, Non-fiction & Poetry',
                               'Science Fiction & Fantasy'],
                'summary': 'The Gregg family loves hunting, but their eight-year-old '
                           "neighbor can't stand it. After countless pleas for them to stop "
                           'are ignored, she has no other choice -- she has to put her magic '
                           'finger on them. Now the Greggs are a family of birds, and like '
                           "it or not, they're going to find out how it feels to be on the "
                           'other end of the gun.'
            }
        ]
        search_results = {
            'total_results': 1,
            'total_pages': 1,
            'results': book_results
        }
        responses.get(
            url='https://book-finder1.p.rapidapi.com/api/search',
            json=search_results,
            status=200
        )
        user_input = {
            'author': 'Roald Dahl',
            'categories': 'Fiction, Non-fiction & Poetry',
            'book_type': 'Fiction',
            'book_num': 1}
        self.assertEqual(self.internal_api.search_book_suggestions(user_input=user_input), book_results)
        # mock_get_all_books.assert_has_calls([call('read_books'), call('to_read_books')])

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('The Witches', 'Roald Dahl', 'Science Fiction & Fantasy')
                    ]
                ))
    @responses.activate
    def test_search_book_suggestion_if_API_returns_book_on_read_list(self, mock_get_all_books):
        self.internal_api = InternalAPI()
        book_results = [
            {
                'authors': ['Toshikazu Kawaguchi'],
                'title': 'Before the coffee gets cold',
                'categories': ['fiction'],
                'summary': ''
            }
        ]
        search_results = {
            'total_results': 1,
            'total_pages': 1,
            'results': book_results
        }
        responses.get(
            url='https://book-finder1.p.rapidapi.com/api/search',
            json=search_results,
            status=200
        )
        user_input = {
            'author': 'Toshikazu Kawaguchi',
            'categories': '',
            'book_type': 'Fiction',
            'book_num': 1}
        with self.assertRaises(Exception):
            self.internal_api.search_book_suggestions(user_input)

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('The Witches', 'Roald Dahl', 'Science Fiction & Fantasy')
                    ]
                ))
    @responses.activate
    def test_search_book_suggestion_returns_right_number_of_books(self, mock_get_all_books):
        self.internal_api = InternalAPI()
        book_results = [
            {
                'authors': ['Roald Dahl'],
                'title': 'The Magic Finger',
                'categories': ['Hobbies, Sports & Outdoors',
                               'Fiction, Non-fiction & Poetry',
                               'Science Fiction & Fantasy'],
                'summary': 'The Gregg family loves hunting, but their eight-year-old '
                           "neighbor can't stand it. After countless pleas for them to stop "
                           'are ignored, she has no other choice -- she has to put her magic '
                           'finger on them. Now the Greggs are a family of birds, and like '
                           "it or not, they're going to find out how it feels to be on the "
                           'other end of the gun.'
            },
            {
                'authors': ['Roald Dahl'],
                'categories': ['Animals, Bugs & Pets',
                               'Fiction, Non-fiction & Poetry',
                               'Science Fiction & Fantasy'],
                'summary': 'In this book you will find: Boggis an enormously fat man, a '
                           'chicken farmer and a mean man. Bunce, a pot bellied dwarf, a '
                           'duck-and-goose farmer and a nasty man. Bean, a thin man, a '
                           'turkey-and-apple farmer and a beastly man. Badger, the most '
                           'respectable and well-behaved animal in the district. Rat, a rude '
                           'creature and a drunkard, and also a Mrs. Fox and her four '
                           'children.',
                'title': 'Fantastic Mr. Fox'
            },

            {
                'authors': ['Roald Dahl'],
                'categories': ['Real Life',
                               'Fiction, Non-fiction & Poetry',
                               'Science Fiction & Fantasy'],
                'summary': 'Georgeas grouchy grandma needs a taste of her own medicine, and '
                           'George knows just the right ingredients to put into it!',

                'title': "George's Marvelous Medicine"},
            {'authors': ['Roald Dahl'],
             'categories': ['Fiction, Non-fiction & Poetry',
                            'Animals, Bugs & Pets',
                            'Science Fiction & Fantasy'],
             'summary': 'Originally published: [New York]: Alfred A. Knopf, 1970.',
             'title': 'Fantastic Mr. Fox'
             },
            {
                'authors': ['Roald Dahl'],
                'categories': ['Fiction, Non-fiction & Poetry', 'Science Fiction & Fantasy'],
                'summary': 'Mr. Willy Wonka might be a genius with chocolate, but Charlie and '
                           "his family don't trust his flying skills one bit. And right now, "
                           "he's at the helm of a giant glass elevator that's picking up "
                           'speed and hurtling through space -- with Charlie and the entire '
                           "Bucket family stuck inside! Roald Dahl's uproarious sequel to "
                           '"Charlie and the Chocolate Factory" is certain to delight and '
                           'entertain a new generation of readers. "From the Hardcover '
                           'edition."',
                'title': 'Charlie and the Great Glass Elevator'
            }
        ]
        search_results = {
            'total_results': 4,
            'total_pages': 1,
            'results': book_results
        }
        responses.get(
            url='https://book-finder1.p.rapidapi.com/api/search',
            json=search_results,
            status=200
        )
        user_input = {
            'author': 'Toshikazu Kawaguchi',
            'categories': '',
            'book_type': 'Fiction',
            'book_num': 2}
        expected = user_input['book_num']
        result = len(self.internal_api.search_book_suggestions(user_input))
        self.assertEqual(result, expected)

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('The Witches', 'Roald Dahl', 'Science Fiction & Fantasy')
                    ]
                ))
    @responses.activate
    def test_search_book_suggestion_returns_books_even_though_results_give_less_than_asked_for(self,
                                                                                               mock_get_all_books):
        self.internal_api = InternalAPI()
        book_results = [
            {
                'authors': ['Roald Dahl'],
                'title': 'The Magic Finger',
                'categories': ['Hobbies, Sports & Outdoors',
                               'Fiction, Non-fiction & Poetry',
                               'Science Fiction & Fantasy'],
                'summary': 'The Gregg family loves hunting, but their eight-year-old '
                           "neighbor can't stand it. After countless pleas for them to stop "
                           'are ignored, she has no other choice -- she has to put her magic '
                           'finger on them. Now the Greggs are a family of birds, and like '
                           "it or not, they're going to find out how it feels to be on the "
                           'other end of the gun.'
            }
        ]
        search_results = {
            'total_results': 1,
            'total_pages': 1,
            'results': book_results
        }
        responses.get(
            url='https://book-finder1.p.rapidapi.com/api/search',
            json=search_results,
            status=200
        )
        user_input = {
            'author': 'Roald Dahl',
            'categories': 'Fiction, Non-fiction & Poetry',
            'book_type': 'Fiction',
            'book_num': 4}
        expected = search_results['total_results']
        result = len(self.internal_api.search_book_suggestions(user_input))
        self.assertEqual(result, expected)

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('The Witches', 'Roald Dahl', 'Science Fiction & Fantasy')
                    ]
                )
                )
    def test_check_for_duplicates_from_read_list_when_no_duplicates(self, mock_get_all_books):
        self.internal_api = InternalAPI()
        book_suggestions = [
            {
                'authors': ['Roald Dahl'],
                'title': 'The Magic Finger',
                'categories': ['Hobbies, Sports & Outdoors',
                               'Fiction, Non-fiction & Poetry',
                               'Science Fiction & Fantasy'],
                'summary': 'The Gregg family loves hunting, but their eight-year-old '
                           "neighbor can't stand it. After countless pleas for them to stop "
                           'are ignored, she has no other choice -- she has to put her magic '
                           'finger on them. Now the Greggs are a family of birds, and like '
                           "it or not, they're going to find out how it feels to be on the "
                           'other end of the gun.'
            }
        ]
        expected = book_suggestions
        result = self.internal_api.check_for_duplicates_from_read_list(book_suggestions)
        self.assertEqual(expected, result)

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('The Witches', 'Roald Dahl', 'Science Fiction & Fantasy')
                    ]
                )
                )
    def test_check_for_duplicates_from_read_list_when_one_duplicate(self, mock_get_all_books):
        self.internal_api = InternalAPI()
        book_suggestions = [
            {
                'authors': ['Toshikazu Kawaguchi'],
                'title': 'Before the coffee gets cold',
                'categories': ['fiction'],
                'summary': ''
            }
        ]
        expected = []
        result = self.internal_api.check_for_duplicates_from_read_list(book_suggestions)
        self.assertEqual(expected, result)

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('The Witches', 'Roald Dahl', 'Science Fiction & Fantasy')
                    ]
                )
                )
    def test_check_for_duplicates_from_read_list_when_multiple_duplicates(self, mock_get_all_books):
        self.internal_api = InternalAPI()
        book_suggestions = [
            {
                'authors': ['Toshikazu Kawaguchi'],
                'title': 'Before the coffee gets cold',
                'categories': ['fiction'],
                'summary': ''
            },
            {
                'authors': ['Malcolm Gladwell'],
                'title': 'Talking to strangers',
                'categories': ['nonfiction'],
                'summary': ''
            }
        ]
        expected = []
        result = self.internal_api.check_for_duplicates_from_read_list(book_suggestions)
        self.assertEqual(expected, result)

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('The Witches', 'Roald Dahl', 'Science Fiction & Fantasy')
                    ]
                )
                )
    def test_check_for_duplicates_from_to_read_list_when_no_duplicates(self, mock_get_all_books):
        self.internal_api = InternalAPI()
        book_suggestions = [
            {
                'authors': ['Toshikazu Kawaguchi'],
                'title': 'Before the coffee gets cold',
                'categories': ['fiction'],
                'summary': ''
            }
        ]
        expected = book_suggestions
        result = self.internal_api.check_for_duplicates_from_to_read_list(1, book_suggestions)
        self.assertEqual(expected, result)

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('The Witches', 'Roald Dahl', 'Science Fiction & Fantasy')
                    ]
                )
                )
    def test_check_for_duplicates_from_to_read_list_when_one_duplicate(self, mock_get_all_books):
        self.internal_api = InternalAPI()
        book_suggestions = [
            {
                'authors': ['Roald Dahl'],
                'title': 'The Witches',
                'categories': ['Science Fiction & Fantasy'],
                'summary': ''
            }
        ]
        expected = []
        result = self.internal_api.check_for_duplicates_from_to_read_list(1, book_suggestions)
        self.assertEqual(expected, result)

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('The Witches', 'Roald Dahl', 'Science Fiction & Fantasy'),
                        ('The Magic Finger', 'Roald Dahl', 'Hobbies, Sports & Outdoors')
                    ]
                )
                )
    def test_check_for_duplicates_from_to_read_list_when_multiple_duplicates(self, mock_get_all_books):
        self.internal_api = InternalAPI()
        book_suggestions = [
            {
                'authors': ['Roald Dahl'],
                'title': 'The Witches',
                'categories': ['Science Fiction & Fantasy'],
                'summary': ''
            },
            {
                'authors': ['Roald Dahl'],
                'title': 'The Magic Finger',
                'categories': ['Hobbies, Sports & Outdoors',
                               'Fiction, Non-fiction & Poetry',
                               'Science Fiction & Fantasy'],
                'summary': 'The Gregg family loves hunting, but their eight-year-old '
                           "neighbor can't stand it. After countless pleas for them to stop "
                           'are ignored, she has no other choice -- she has to put her magic '
                           'finger on them. Now the Greggs are a family of birds, and like '
                           "it or not, they're going to find out how it feels to be on the "
                           'other end of the gun.'
            }
        ]
        expected = []
        result = self.internal_api.check_for_duplicates_from_to_read_list(1, book_suggestions)
        self.assertEqual(expected, result)

    @responses.activate
    def test_random_book_suggestion(self):
        self.internal_api = InternalAPI()
        book_results = [
            {
                'authors': ['Roald Dahl'],
                'title': 'The Magic Finger',
                'categories': ['Hobbies, Sports & Outdoors',
                               'Fiction, Non-fiction & Poetry',
                               'Science Fiction & Fantasy'],
                'summary': 'The Gregg family loves hunting, but their eight-year-old '
                           "neighbor can't stand it. After countless pleas for them to stop "
                           'are ignored, she has no other choice -- she has to put her magic '
                           'finger on them. Now the Greggs are a family of birds, and like '
                           "it or not, they're going to find out how it feels to be on the "
                           'other end of the gun.'
            }
        ]
        search_results = {
            'total_results': 1,
            'total_pages': 1,
            'results': book_results
        }
        responses.get(
            url='https://book-finder1.p.rapidapi.com/api/search',
            json=search_results,
            status=200
        )
        user_input = {
            'categories': 'Fiction, Non-fiction & Poetry',
        }
        book_results[0]['authors'] = ', '.join(book_results[0]['authors'])
        book_results[0]['categories'] = ', '.join(book_results[0]['categories'])
        expected = book_results[0]
        result = self.internal_api.random_book_suggestion(user_input)
        self.assertEqual(expected, result)

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('Dirty Beasts', 'Roald Dahl', 'Fiction, Non-fiction & Poetry'),
                        ('The Magic Finger', 'Roald Dahl', 'Hobbies, Sports & Outdoors')
                    ]
                )
                )
    @mock.patch("src.Database.db_utils.insert_book")
    def test_add_to_to_read_list_when_adding_a_book(self, mock_insert_book, mock_get_all_books):
        self.internal_api = InternalAPI()
        to_read = {
            'authors': ['Khaled Hosseini'],
            'title': 'Sea Prayer',
            'categories': ['Mystery & Suspense']
        }
        expected = 'Sea Prayer has been added to reading list'
        result = self.internal_api.add_to_to_read_list(to_read)
        mock_insert_book.assert_called_once_with(
            table='to_read_books', title=to_read['title'], author=to_read['authors'], category=to_read['categories']
        )
        self.assertEqual(expected, result)

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('Dirty Beasts', 'Roald Dahl', 'Fiction, Non-fiction & Poetry'),
                        ('The Magic Finger', 'Roald Dahl', 'Hobbies, Sports & Outdoors')
                    ]
                )
                )
    @mock.patch("src.Database.db_utils.insert_book")
    def test_add_to_to_read_list_when_book_already_on_table(self, mock_insert_book, mock_get_all_books):
        self.internal_api = InternalAPI()
        to_read = {
            'authors': ['Roald Dahl'],
            'title': 'Dirty Beasts',
            'categories': ['Fiction, Non-fiction & Poetry']
        }
        with self.assertRaises(BookAlreadyOnTable):
            self.internal_api.add_to_to_read_list(to_read)

        mock_insert_book.assert_not_called()

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('Dirty Beasts', 'Roald Dahl', 'Fiction, Non-fiction & Poetry'),
                        ('The Magic Finger', 'Roald Dahl', 'Hobbies, Sports & Outdoors')
                    ]
                )
                )
    @mock.patch("src.Database.db_utils.insert_book")
    def test_add_to_read_list_when_adding_a_book(self, mock_insert_book, mock_get_all_books):
        self.internal_api = InternalAPI()
        read = {
            'author': ['Khaled Hosseini'],
            'title': 'Sea Prayer',
            'categories': ['Mystery & Suspense']
        }
        expected = 'Sea Prayer has been added to the books read list'
        result = self.internal_api.add_to_read_list(read)
        mock_insert_book.assert_called_once_with(
            table='read_books', title=read['title'], author=read['author'], category=read['categories']
        )
        self.assertEqual(expected, result)

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('Dirty Beasts', 'Roald Dahl', 'Fiction, Non-fiction & Poetry'),
                        ('The Magic Finger', 'Roald Dahl', 'Hobbies, Sports & Outdoors')
                    ]
                )
                )
    @mock.patch("src.Database.db_utils.insert_book")
    def test_add_to_read_list_when_book_already_on_table(self, mock_insert_book, mock_get_all_books):
        self.internal_api = InternalAPI()
        read = {
            'authors': ['Roald Dahl'],
            'title': 'The B.F.G',
            'categories': ['Animals, Bugs & Pets']
        }
        with self.assertRaises(BookAlreadyOnTable):
            self.internal_api.add_to_read_list(read)

        mock_insert_book.assert_not_called()

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('Dirty Beasts', 'Roald Dahl', 'Fiction, Non-fiction & Poetry'),
                        ('The Magic Finger', 'Roald Dahl', 'Hobbies, Sports & Outdoors')
                    ]
                )
                )
    @mock.patch("src.Database.db_utils.delete_book")
    def delete_from_to_read_list_when_book_is_on_list(self, mock_delete_book, mock_get_all_books):
        self.internal_api = InternalAPI()
        title = 'Dirty Beasts'
        expected = 'Dirty Beasts has been deleted from the to-read list'
        result = self.internal_api.delete_from_to_read_list(title)

        mock_delete_book.assert_called_once_with(
            table='to_read_books'
        )
        self.assertEqual(expected, result)

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('Dirty Beasts', 'Roald Dahl', 'Fiction, Non-fiction & Poetry'),
                        ('The Magic Finger', 'Roald Dahl', 'Hobbies, Sports & Outdoors')
                    ]
                )
                )
    @mock.patch("src.Database.db_utils.delete_book")
    def test_delete_from_to_read_list_when_book_not_on_list(self, mock_delete_book, mock_get_all_books):
        self.internal_api = InternalAPI()
        title = 'The girl on the train'

        with self.assertRaises(BookNotFound):
            self.internal_api.delete_from_to_read_list(title)

        mock_delete_book.assert_not_called()

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('Dirty Beasts', 'Roald Dahl', 'Fiction, Non-fiction & Poetry'),
                        ('The Magic Finger', 'Roald Dahl', 'Hobbies, Sports & Outdoors')
                    ]
                )
                )
    @mock.patch("src.Database.db_utils.delete_book")
    def test_delete_from_read_list_when_book_is_on_list(self, mock_delete_book, mock_get_all_books):
        self.internal_api = InternalAPI()
        title = 'Before the coffee gets cold'
        expected = 'Before the coffee gets cold has been deleted from the read list'
        result = self.internal_api.delete_from_read_list(title)

        mock_delete_book.assert_called_once_with(
            table='read_books', book_title=title
        )
        self.assertEqual(expected, result)

    @mock.patch("src.Database.db_utils.get_all_books",
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('Dirty Beasts', 'Roald Dahl', 'Fiction, Non-fiction & Poetry'),
                        ('The Magic Finger', 'Roald Dahl', 'Hobbies, Sports & Outdoors')
                    ]
                )
                )
    @mock.patch("src.Database.db_utils.delete_book")
    def test_delete_from_read_list_when_book_not_on_list(self, mock_delete_book, mock_get_all_books):
        self.internal_api = InternalAPI()
        title = 'The girl on the train'

        with self.assertRaises(BookNotFound):
            self.internal_api.delete_from_read_list(title)

        mock_delete_book.assert_not_called()

    @mock.patch('src.Database.db_utils.get_all_books',
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('Dirty Beasts', 'Roald Dahl', 'Fiction, Non-fiction & Poetry'),
                        ('The Magic Finger', 'Roald Dahl', 'Hobbies, Sports & Outdoors')
                    ]
                )
                )
    def test_get_read_list_returns_list(self, mock_get_all_books):
        self.internal_api = InternalAPI()
        result = self.internal_api.get_read_list()
        expected = [
            ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
             'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
            ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
            ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
            ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')

        ]
        self.assertEqual(result, expected)

    @mock.patch('src.Database.db_utils.get_all_books',
                side_effect=mock_db_responses(
                    read=[
                        ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction',
                         'I loved the atmosphere in the book, so dreamy, but also full of emotions', '4'),
                        ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
                        ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book! ', '4'),
                        ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
                    ],
                    to_read=[
                        ('Dirty Beasts', 'Roald Dahl', 'Fiction, Non-fiction & Poetry'),
                        ('The Magic Finger', 'Roald Dahl', 'Hobbies, Sports & Outdoors')
                    ]
                )
                )
    def test_get_to_read_list_returns_list(self, mock_get_all_books):
        self.internal_api = InternalAPI()
        result = self.internal_api.get_to_read_list()
        expected = [
            ('Dirty Beasts', 'Roald Dahl', 'Fiction, Non-fiction & Poetry'),
            ('The Magic Finger', 'Roald Dahl', 'Hobbies, Sports & Outdoors')
        ]
        self.assertEqual(result, expected)

    @mock.patch('src.Database.db_utils.get_all_books')
    @mock.patch('src.Database.db_utils.update_review')
    def test_add_a_review_for_book_on_list(self, mock_update_review, mock_get_all_books):
        self.internal_api = InternalAPI()
        mock_get_all_books.return_value = [
            ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction', 'I loved the atmosphere...', '4'),
            ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', None, '5'),
            ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book!', '4'),
            ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
        ]

        internal_api = InternalAPI()

        read = {
            'authors': ['Malcolm Gladwell'],
            'title': 'Talking to strangers',
            'categories': ['nonfiction']
        }
        user_review = 'The book was great!'
        result = internal_api.add_a_review(read, user_review)

        # Assert that the update_review function was called with the correct arguments
        mock_update_review.assert_called_once_with('Talking to strangers', 'The book was great!')

        # Assert that the result matches the return value of update_review
        self.assertEqual(result, mock_update_review.return_value)

    @mock.patch('src.Database.db_utils.get_all_books')
    def test_add_a_review_book_not_found(self, mock_get_all_books):
        self.internal_api = InternalAPI()
        mock_get_all_books.return_value = [
            ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction', 'I loved the atmosphere...', '4'),
            ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book!', '4'),
            ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
        ]
        read = {
            'authors': ['Malcolm Gladwell'],
            'title': 'Talking to strangers',
            'categories': ['nonfiction']
        }
        user_review = 'Fantastic'
        with self.assertRaises(BookNotFound):
            self.internal_api.add_a_review(read, user_review)


    @mock.patch('src.Database.db_utils.get_all_books')
    @mock.patch('src.Database.db_utils.update_rating')
    def test_add_a_star_rating_for_book_on_list(self, mock_update_rating, mock_get_all_books):
        self.internal_api = InternalAPI()
        mock_get_all_books.return_value = [
            ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction', 'I loved the atmosphere...', '4'),
            ('Talking to strangers', 'Malcolm Gladwell', 'nonfiction', 'It was good!', None),
            ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book!', '4'),
            ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
        ]

        internal_api = InternalAPI()

        read = {
            'authors': ['Malcolm Gladwell'],
            'title': 'Talking to strangers',
            'categories': ['nonfiction']
        }
        user_rating = '5'
        result = internal_api.add_star_rating(read, user_rating)
        mock_update_rating.assert_called_once_with('Talking to strangers', '5')
        self.assertEqual(result, mock_update_rating.return_value)

    @mock.patch('src.Database.db_utils.get_all_books')
    def test_add_a_star_rating_book_not_found(self, mock_get_all_books):
        self.internal_api = InternalAPI()
        mock_get_all_books.return_value = [
            ('Before the coffee gets cold', 'Toshikazu Kawaguchi', 'fiction', 'I loved the atmosphere...', '4'),
            ('The B.F.G', 'Roald Dahl', 'Animals, Bugs & Pets', 'Really enjoyed this book!', '4'),
            ('Wilderness tips', 'Margaret Atwood', 'fiction', 'A short stories anthology', '3')
        ]
        read = {
            'authors': ['Malcolm Gladwell'],
            'title': 'Talking to strangers',
            'categories': ['nonfiction']
        }
        user_rating = 5
        with self.assertRaises(BookNotFound):
            self.internal_api.add_star_rating(read, user_rating)


if __name__ == "__main__":
    main()
