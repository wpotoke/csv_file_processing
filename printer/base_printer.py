from abc import ABC, abstractmethod


class BasePrint(ABC):

    @abstractmethod
    def print(self, data: list[dict[str, str | float]]) -> None:
        """Выводит данные в консоль."""

    def check_items(self, data):
        if not data:
            raise ValueError("No data to print: the data object is empty. Check your params of filter or order")
        