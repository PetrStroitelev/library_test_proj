from typing import NoReturn, final

from app.app_exception import AppException
from app.app_exception_type import AppExceptionType
from model.book_status import BookStatus


@final
class Helper(object):

    @staticmethod
    def print_ex(ex: Exception) -> NoReturn:
        print(f'\033[31m{str(ex)}\033[0m')

    @staticmethod
    def get_status(val: str) -> BookStatus:
        match val:
            case "1":
                return BookStatus.InStock
            case "2":
                return BookStatus.Received
            case _:
                raise AppException('Ошибка статуса', AppExceptionType.INCORRECT_STATUS)
