import requests
import random
from itertools import takewhile

endpoint = 'https://book-finder1.p.rapidapi.com/api/search'

choice = input("Hello! How can I help you today? Do you know what you're after or would you want me to pick something for you? (Type 'I know' or 'pick something' as an answer)\n> ")

# Get all the books from the API
# This actually could be the main OOP class for calling APIs

category = {1: "Animals, Bugs & Pets", 2: "Art, Creativity & Music", 3: "General Literature", 4: "Hobbies",
            5: "Sports & Outdoors", 6: "Science Fiction & Fantasy", 7: "Real Life", 8: "Science & Technology",
            9: "Mystery & Suspense", 10: "Reference"}
book_type = {1: "Fiction", 2: "Nonfiction"}
def find_all_books(category, book_type):

    random_category = random.randrange(1, 10)
    random_book_type = random.randrange(1, 2)
    search = {
        'book_type': book_type[random_book_type],
        'results_per_page': '100',
        'page': '1',
        'categories': category[random_category]
    }

    requirement = {
    'X-RapidAPI-Key': 'e42255e58dmsh896e188a4c3b74dp12368fjsn273ec0f1d7ca',
    'X-RapidAPI-Host': 'book-finder1.p.rapidapi.com'
    }

    response = requests.get(endpoint, params=search, headers=requirement)
    records = response.json()
    list_records = []

    for page in range(records['total_pages']):
        search["page"] = page + 1
        response = requests.get(endpoint, params=search, headers=requirement)
        list_records.append(response.json())

    # pick pages which have records in them (bypassing the limitations)
    list_records_valid = takewhile(lambda x: x != {'message': 'You have exceeded the rate limit per second for your plan, BASIC, by the API provider'}, list_records)

    list_records_valid = list(list_records_valid)

    output_list = []

    # combine all records from the available pages into a single list
    for i in range(len(list_records_valid)):
        output_list.extend(list_records_valid[i]['results'])

    return output_list


# API filtering function

def book_filtering_function(category, book_type):
    category_input = input("\nWhat category books are you interested in? Please, select the number of the option:\n1. Animals, Bugs & Pets,\n2. Art,Creativity & Music,\n3. General Literature,\n4. Hobbies,\n5. Sports & Outdoors,\n6. Science Fiction & Fantasy,\n7. Real Life,\n8. Science & Technology,\n9. Mystery & Suspense,\n10. Reference\n> ")
    book_type_input = input("\nWhat type of books are you interested in? Please, select the number of the option:\n1. Fiction,\n2. Nonfiction\n> ")
    # could add more filters ...

    search = {
        # 'series': "Wings of fire",
        # 'author': 'J. K. Rowling',
        # 'lexile_min': '600',
        'book_type': book_type[int(book_type_input)],
        # 'lexile_max': '800',
        'results_per_page': '100',
        'page': '1',
        'categories': category[int(category_input)]
    }

    requirement = {
    'X-RapidAPI-Key': 'e42255e58dmsh896e188a4c3b74dp12368fjsn273ec0f1d7ca',
    'X-RapidAPI-Host': 'book-finder1.p.rapidapi.com'
    }

    response = requests.get(endpoint, params=search, headers=requirement)
    records = response.json()
    list_records = []


    for page in range(records['total_pages']):
        search["page"] = page + 1
        response = requests.get(endpoint, params=search, headers=requirement)
        list_records.append(response.json())

    # pick pages which have records in them (bypassing the limitations)
    list_records_valid = takewhile(lambda x: x != {'message': 'You have exceeded the rate limit per second for your plan, BASIC, by the API provider'}, list_records)

    list_records_valid = list(list_records_valid)

    output_list = []

    # combine all records from the available pages into a single list
    for i in range(len(list_records_valid)):
        output_list.extend(list_records_valid[i]['results'])

    # 10 random options from the list
    random_sample = random.sample(output_list, 10)

    return random_sample


if choice == 'I know':
    print("Good for you!")
    filtered_output = book_filtering_function(category, book_type)
    print("\nHere you go:")
    for i in range(len(filtered_output)):
        print(f"Option {i+1}: Author: {filtered_output[i]['authors'][0]}, Title: {filtered_output[i]['title']}, Summary: {filtered_output[i]['summary']}")
else:
    print("Wait, brb")
    all_the_books = find_all_books(category, book_type)
    random_num = random.randrange(0, (len(all_the_books) -1))
    print(f"The book I've picked for you:\nAuthor: {all_the_books[random_num]['authors'][0]},\nTitle: {all_the_books[random_num]['title']},\nSummary: {all_the_books[random_num]['summary']}")



