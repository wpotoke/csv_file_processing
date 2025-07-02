from tabulate import tabulate
from printer.base_printer import BasePrint


class TablePrettyPrint(BasePrint):

    def print(self, data: list[dict[str, str | float | int]]) -> None:
        """Выводит данные в виде таблицы."""

        super().check_items(data)
        table = [field.values() for field in data]
        headers = [i for i in data[0]]
        print(tabulate(table, headers, tablefmt="pretty"))
