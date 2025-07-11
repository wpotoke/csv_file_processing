from abc import ABC, abstractmethod
from mixins.mixin_eror.no_data_mixin import NoDataMixin
from printer.table_printer import TablePrettyPrint


class BaseOrderBy(TablePrettyPrint, ABC, NoDataMixin):
    def check_type(self, field: dict[str, str | float], field_order: str) -> None:
        try:
            float(field[field_order])
        except ValueError:
            raise TypeError(f"Cannot sort by non-numeric field '{field_order}'.")

    @abstractmethod
    def order_by(self, data, field_order) -> list[dict[str, str | float]]:
        """Сортирует данные по указанному полю."""


class OrderByDesc(BaseOrderBy):
    def order_by(
        self, data: list[dict[str, str | float]], field_order: str
    ) -> list[dict[str, str | float]]:
        """Сортирует данные по убыванию по указанному полю."""

        super().check_items(data)
        for field in data:
            super().check_type(field, field_order)
        return sorted(data, key=lambda field: float(field[field_order]), reverse=True)


class OrderByAsc(BaseOrderBy):
    def order_by(
        self, data: list[dict[str, str | float]], field_order: str
    ) -> list[dict[str, str | float]]:
        """Сортирует данные по возрастанию по указанному полю."""

        super().check_items(data)
        for field in data:
            super().check_type(field, field_order)
        return sorted(data, key=lambda field: float(field[field_order]))
