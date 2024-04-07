from pathlib import Path
from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message


class DocumentType(BaseFilter):
    file_types = None

    def __init__(self, file_types: List[str]):
        self.file_types = file_types

    async def __call__(self, message: Message, *args, **kwargs):
        if message.document:
            if Path(message.document.file_name).suffix in self.file_types:
                return True

        return False
