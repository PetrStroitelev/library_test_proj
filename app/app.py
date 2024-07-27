import re
from datetime import datetime
from typing import final

from api.api import Api
from app.app_exception import AppException
from app.app_exception_type import AppExceptionType
from base.helper import Helper


@final
class App(object):
    def __init__(self, db_path: str = None):
        self.api = Api(db_path)

    def _check_empty_field(self, value: str) -> None:
        if len(value) == 0:
            raise AppException('Данное поле не может быть пустым', AppExceptionType.NONE_EMPTY_FIELD)

    def _check_author_name(self, name: str) -> None:
        regexp_result = re.match(r'^([a-zA-Z]+\s*)*[a-zA-Z]+$', name)
        if regexp_result is None:
            raise AppException('В имени автора не должно быть цифр и лишних символов',
                               AppExceptionType.INCORRECT_AUTHOR_NAME)

    def _check_year(self, year: str) -> None:
        year = int(year)
        current_year = datetime.now().year
        if 1900 > year or year > current_year:
            raise AppException(f"Год произведения должен составлять число в диапозоне от 1900 до {current_year}",
                               AppExceptionType.INCORRECT_YEAR)

    def _add_book(self) -> None:
        try:
            title = input('Введите название книги: ').strip()
            self._check_empty_field(title)

            author = input('Введите автора книги: ').strip()
            self._check_empty_field(author)
            self._check_author_name(author)

            year = input('Введите год создания произведения: ').strip()
            self._check_empty_field(year)
            self._check_year(year)

            if self.api.add_book(title, author, year) is False:
                raise AppException('Ошибка API', AppExceptionType.API_EXCEPTION)
        except Exception as ex:
            Helper.print_ex(ex)

    def _delete_book(self) -> None:
        try:
            id_del_book = input('Введите ID книги, которую необходимо удалить: ').strip()
            self._check_empty_field(id_del_book)

            if self.api.delete_book(id_del_book) is False:
                raise AppException('Ошибка удаления', AppExceptionType.API_EXCEPTION)
        except Exception as ex:
            Helper.print_ex(ex)

    def _search_book(self) -> None:
        try:
            search: str = ""

            while search != "0":
                search = input('''
            Введите цифру, соответствующую способу поиска:
                1. По названию книги
                2. По имени автора
                3. По году создания

                0. Выйти из поиска книги\n''')

                match search:
                    case "0":
                        print('\033[36mОсуществлен выход из поиска книг.\033[0m')
                    case "1":
                        title = input('Введите название книги: ')
                        self._check_empty_field(title)
                        result = self.api.search_by_field("title", title)
                        if result is not None:
                           self._show_books(result)
                    case "2":
                        author = input('Введите имя автора: ').strip()
                        self._check_empty_field(author)
                        self._check_author_name(author)
                        result = self.api.search_by_field("author", author)
                        if result is not None:
                            self._show_books(result)
                    case "3":
                        year = input('Введите год создания произведения: ').strip()
                        self._check_empty_field(year)
                        self._check_year(year)
                        result = self.api.search_by_field('year', year)
                        if result is not None:
                            self._show_books(result)
                    case _:
                         print('''\033[31mВведено некорректное значение!!! # Повторите ввод.\033[0m''')
        except Exception as ex:
            Helper.print_ex(ex)

    def _show_books(self, result: dict) -> None:
        library_ = result
        max_length_title: int = 9
        max_length_author: int = 6

        for books in library_['books']:
            books_len_title: int = len(books['title'])
            books_len_author: int = len(books['author'])
            max_length_title = books_len_title if (max_length_title < books_len_title) else max_length_title
            max_length_author = books_len_author if (max_length_author < books_len_author) else max_length_author

        print("{:<10} {:<{max_length_title}} {:<{max_length_author}} {:<5} {:<10}".format('ID', 'Название', 'Автор',
                                                                                          'Год',
                                                                                          'Статус',
                                                                                          max_length_title=max_length_title + 1,
                                                                                          max_length_author=max_length_author + 1))

        for books in library_['books']:
            print(
                "{:<10} {:<{max_length_title}} {:<{max_length_author}} {:<5} {:<10}".format(books['id'], books['title'],
                                                                                            books['author'],
                                                                                            books["year"],
                                                                                            books["status"],
                                                                                            max_length_title=max_length_title + 1,
                                                                                            max_length_author=max_length_author + 1))

    def _change_book_status(self) -> None:
        try:
            id_book = input('Введите ID книги, которой необходимо сменить статус: ')
            self._check_empty_field(id_book)

            status = input('Введите новый статус для книги: 1 - в наличии, 2 - выдана')
            self._check_empty_field(status)

            if self.api.change_status(id_book, Helper.get_status(status)) is False:
                raise AppException('Ошибка смены статуса', AppExceptionType.API_EXCEPTION)

        except Exception as ex:
            Helper.print_ex(ex)

    def start(self):
        choice: str = ""
        while choice != "0":
            print('''
        Введите цифру, соответствующую необходимому действию:
            1. Добавить книгу
            2. Удалить книгу
            3. Найти книгу
            4. Отобразить все книги
            5. Измененить статус книги

            0. Закончить работу с приложением''')

            choice = input()
            match choice:
                case "0":
                    print('\033[36mОсуществлен выход из системы.\033[0m')
                case "1":
                    self._add_book()
                case "2":
                    self._delete_book()
                case "3":
                    self._search_book()
                case "4":
                    self._show_books(self.api.get_library)
                case "5":
                    self._change_book_status()
                case _:
                    print('''\033[31mВведено некорректное значение!!! Повторите ввод.\033[0m''')
