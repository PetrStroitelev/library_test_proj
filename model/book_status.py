from enum import Enum
from typing import final


@final
class BookStatus(Enum):
    InStock = 0
    Received = 1

    def __str__(self):
        if self.name == "InStock":
            return "в наличии"

        if self.name == "Received":
            return "выдана"
