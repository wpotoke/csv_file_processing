from typing import Any, Callable
from abc import ABC, abstractmethod


class BaseReader(ABC):

    @abstractmethod
    def read(self, file_name: str) -> list[dict[str, str]]:
        """Читает данные из файла и возвращает список словарей."""
