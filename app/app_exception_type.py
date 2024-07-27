from enum import Enum
from typing import final


@final
class AppExceptionType(Enum):

    NONE_EMPTY_FIELD = 0
    INCORRECT_AUTHOR_NAME = 1
    INCORRECT_YEAR = 2
    API_EXCEPTION = 3
    INCORRECT_STATUS = 4
