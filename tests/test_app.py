import io
import unittest
from unittest.mock import patch

from app.app import App
from app.app_exception import AppException
from app.app_exception_type import AppExceptionType
from test_helper import TestHelper


class TestApp(unittest.TestCase):

    def setUp(self):
        TestHelper.prepare_test_data()
        self.app = App(TestHelper.db_path())

    def test_check_empty_field_no_exception(self):
        self.app._check_empty_field("123")

    def test_check_empty_field_exception(self):
        with self.assertRaises(AppException) as ex:
            self.app._check_empty_field("")

        self.assertEqual(str(ex.exception), "Данное поле не может быть пустым")
        self.assertEqual(ex.exception.error_type, AppExceptionType.NONE_EMPTY_FIELD)

    def test_check_author_name_no_exception(self):
        self.app._check_author_name("ASD")

    def test_check_author_name_exception(self):
        with self.assertRaises(AppException) as ex:
            self.app._check_author_name("12345")

        self.assertEqual(str(ex.exception), "В имени автора не должно быть цифр и лишних символов")
        self.assertEqual(ex.exception.error_type, AppExceptionType.INCORRECT_AUTHOR_NAME)

    def test_check_year_no_exception(self):
        self.app._check_year("1990")
        self.app._check_year("2024")

    def test_check_year_exception(self):
        with self.assertRaises(AppException) as ex:
            self.app._check_year("1890")

        self.assertEqual(str(ex.exception), "Год произведения должен составлять число в диапозоне от 1900 до 2024")
        self.assertEqual(ex.exception.error_type, AppExceptionType.INCORRECT_YEAR)

        with self.assertRaises(AppException) as ex:
            self.app._check_year("2025")

        self.assertEqual(str(ex.exception), "Год произведения должен составлять число в диапозоне от 1900 до 2024")
        self.assertEqual(ex.exception.error_type, AppExceptionType.INCORRECT_YEAR)

    def test_add_book(self):
        with patch('app.app.input', create=True) as mock_input:
            with patch('sys.stdout', new_callable=io.StringIO) as mock_print:
                mock_input.side_effect = ['Albert Einstein', 'Albert Einstein', '1978']
                self.app._add_book()
                self.assertEquals(mock_print.getvalue(),
                                  f'\033[36mКнига Albert Einstein Albert Einstein добавлена в систему\033[0m\n')

    def test_delete_book(self):
        with patch('app.app.input', create=True) as mock_input:
            with patch('sys.stdout', new_callable=io.StringIO) as mock_print:
                mock_input.side_effect = ['1']
                self.app._delete_book()
                self.assertEquals(mock_print.getvalue(), f'\033[36mКнига 123 AAA удалена\033[0m\n')

    def test_delete_book_exception(self):
        with patch('app.app.input', create=True) as mock_input:
            with patch('sys.stdout', new_callable=io.StringIO) as mock_print:

                mock_input.side_effect = ['9999']
                self.app._delete_book()
                self.assertEquals(mock_print.getvalue(), '\033[31mКнига с таким значением id -> 9999 отсутсвует в библиотеке.\033[0m\n\033[31mОшибка удаления\033[0m\n')

    def test_change_book_status(self):
        with patch('app.app.input', create=True) as mock_input:
            with patch('sys.stdout', new_callable=io.StringIO) as mock_print:
                mock_input.side_effect = ['1', '1']
                self.app._change_book_status()
                self.assertEquals(mock_print.getvalue(),
                                  '\033[36mСтатус книги 123 AAA обновлен\033[0m\n')

    def tearDown(self):
        TestHelper.clear_test_data()
