from dataclasses import dataclass
from typing import final

from model.book_status import BookStatus


@final
@dataclass()
class BookDataModel:
    id: int
    title: str
    author: str
    year: str
    status: BookStatus = BookStatus.InStock

    def convert_to_dict(self):
        return {'id': self.id, 'title': self.title, 'author': self.author, 'year': self.year, 'status': str(self.status)}
