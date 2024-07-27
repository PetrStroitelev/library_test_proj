from typing import final
from app.app_exception_type import AppExceptionType


@final
class AppException(Exception):

    def __init__(self, message, error_type: AppExceptionType):
        super().__init__(message)
        self.error_type = error_type
