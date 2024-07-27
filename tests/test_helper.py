import json
import os


class TestHelper(object):

    @staticmethod
    def db_path():
        return 'test_db.json'

    @staticmethod
    def prepare_test_data():
        books = {'books': [{'id': 1, 'title': '123', 'author': 'AAA', 'year': '2024', 'status': 'выдана'},
                           {'id': 2, 'title': '1234', 'author': 'AAAB', 'year': '2024', 'status': 'в наличии'}]}
        data = json.dumps(books)
        with open(TestHelper.db_path(), 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def clear_test_data():
        os.remove(TestHelper.db_path())
