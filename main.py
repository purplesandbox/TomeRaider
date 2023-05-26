import db_utils
from internal_api import InternalAPI, BookNotFound, BookAlreadyOnTable, NoSearchResultsWithGivenCriteria
from pprint import pprint as pp
from tabulate import tabulate
from user_interactions import UserInteractions

user1 = UserInteractions()
user1.welcome()