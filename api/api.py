import json
from typing import final

from base.helper import Helper
from model.book_data_model import BookDataModel
from model.book_status import BookStatus


@final
class Api(object):

    def __init__(self, db_file_path: str = None):
        self.db_file_path = db_file_path if db_file_path is not None else 'resources/db.json'
        self._library: dict = self._load_json()
        self._id: int = int(self._library['books'][-1]['id']) + 1

    @property
    def get_library(self) -> dict:
        return self._library

    def _load_json(self) -> dict:
        with open(self.db_file_path, 'r', encoding='utf-8') as file:
            return eval(json.load(file))

    def _write_json(self) -> None:
        data = json.dumps(self._library)
        with open(self.db_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def search_by_field(self, key: str, value: str) -> dict | None:
        elements: dict = {'books': []}
        for book in self._library['books']:
            if str(book[key]) == value:
                elements['books'].append(book)

        result = elements if len(elements['books']) > 0 else None
        if result is None:
            print(f'\033[31mКнига с таким значением {key} -> {value} отсутсвует в библиотеке.\033[0m')

        return result

    def add_book(self, title: str, author: str, year: str) -> bool:
        try:
            model = BookDataModel(id=self._id, title=title, author=author, year=year)
            self._library['books'].append(model.convert_to_dict())
            self._write_json()
            print(f'\033[36mКнига {title} {author} добавлена в систему\033[0m')
            self._id += 1
            return True
        except Exception as ex:
            Helper.print_ex(ex)
            return False

    def delete_book(self, id_: str) -> bool:
        try:
            del_elements: dict = self.search_by_field('id', id_)

            if del_elements is None:
                return False

            del_element: dict = {}
            for element in del_elements['books']:
                del_element.update(element)
                self._library['books'].remove(del_element)

            self._write_json()

            print(f"\033[36mКнига {del_element['title']} {del_element['author']} удалена\033[0m")
        except Exception as ex:
            Helper.print_ex(ex)
            return False

    def change_status(self, id_: str, status: BookStatus) -> bool:
        try:
            change_status_elements: dict = self.search_by_field('id', id_)

            if change_status_elements is None:
                return False

            change_status_elements['books'][0]['status'] = str(status)
            self._write_json()
            print(f"\033[36mСтатус книги {change_status_elements['books'][0]['title']} {change_status_elements['books'][0]['author']} обновлен\033[0m")
        except Exception as ex:
            Helper.print_ex(ex)
            return False
