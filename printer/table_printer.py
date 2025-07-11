from abc import ABC, abstractmethod
from tabulate import tabulate  # type: ignore[import]
from mixins.mixin_eror.no_data_mixin import NoDataMixin


class BasePrint(ABC, NoDataMixin):
    @abstractmethod
    def print(self, data: list[dict[str, str | float]]) -> None:
        """Выводит данные в консоль."""


class TablePrettyPrint(BasePrint):
    def print(self, data: list[dict[str, str | float | int]]) -> None:
        """Выводит данные в виде таблицы."""

        super().check_items(data)
        table = [field.values() for field in data]
        headers = [i for i in data[0]]
        print(tabulate(table, headers, tablefmt="pretty"))
