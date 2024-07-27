import io
import unittest
from unittest import mock

from api.api import Api
from model.book_status import BookStatus
from test_helper import TestHelper


class TestApi(unittest.TestCase):

    def setUp(self):
        TestHelper.prepare_test_data()
        self.api = Api(TestHelper.db_path())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_add_book(self, mock):
        self.api.add_book(title="Три Мушкетера", author='Дюма', year='1968')
        last_book = self.api.get_library['books'][-1]

        self.assertEqual(last_book['id'], 3)
        self.assertEqual(last_book['title'], 'Три Мушкетера')
        self.assertEqual(last_book['author'], 'Дюма')
        self.assertEqual(last_book['year'], '1968')
        self.assertEqual(last_book['status'], 'в наличии')
        self.assertEquals(mock.getvalue(),
                          f'\033[36mКнига Три Мушкетера Дюма добавлена в систему\033[0m\n')

    def test_search_by_field_id(self):
        dict_ = {'id': "1", 'title': '123', 'author': 'AAA', 'year': '2024'}
        for key in dict_:
            search_result = self.api.search_by_field(key, dict_[key])
            self.assertNotEquals(search_result, None)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_search_by_field_none(self, mock):
        search_result = self.api.search_by_field('id', "19999")
        self.assertEquals(search_result, None)
        self.assertEquals(mock.getvalue(),
                          f'\033[31mКнига с таким значением id -> 19999 отсутсвует в библиотеке.\033[0m\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_book(self, mock):
        self.api.delete_book("2")
        last_book = self.api.get_library['books'][-1]
        self.assertEqual(last_book['id'], 1)
        self.assertEquals(mock.getvalue(), f'\033[36mКнига 1234 AAAB удалена\033[0m\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_change_status(self, mock):
        self.api.change_status("1", BookStatus.InStock)
        last_book = self.api.get_library['books'][1]
        self.assertEqual(last_book['status'], "в наличии")
        self.assertEquals(mock.getvalue(), f'\033[36mСтатус книги 123 AAA обновлен\033[0m\n')

    def tearDown(self):
        TestHelper.clear_test_data()
