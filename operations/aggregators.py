from abc import ABC, abstractmethod
from mixins.mixin_eror.no_data_mixin import NoDataMixin
from printer.table_printer import TablePrettyPrint


class BaseAggregate(TablePrettyPrint, ABC, NoDataMixin):
    @abstractmethod
    def aggregate(
        self, data: list[dict[str, str | float]], aggregate_field: str
    ) -> list[dict[str, int | float]]:
        """Выполняет агрегацию данных по заданному полю."""

    def check_type(self, field: dict[str, str | float], field_aggregate: str) -> None:
        """Проверяет, можно ли преобразовать значение поля к числу."""
        try:
            float(field[field_aggregate])
        except ValueError:
            raise TypeError(f"Cannot sort by non-numeric field '{field_aggregate}'.")


class AggregateMin(BaseAggregate):
    def aggregate(
        self, data: list[dict[str, str | float]], aggregate_field: str
    ) -> list[dict[str, float | int]]:
        """Вычисляет минимальное значение по указанному полю."""

        super().check_items(data)
        result = []

        for field in data:
            super().check_type(field, aggregate_field)
            result.append(float(field[aggregate_field]))
        return [{"min": min(result)}]


class AggregateMax(BaseAggregate):
    def aggregate(
        self, data: list[dict[str, str | float]], aggregate_field: str
    ) -> list[dict[str, float | int]]:
        """Вычисляет максимальное значение по указанному полю."""

        super().check_items(data)
        result = []

        for field in data:
            super().check_type(field, aggregate_field)
            result.append(float(field[aggregate_field]))
        return [{"max": max(result)}]


class AggregateAvg(BaseAggregate):
    def aggregate(
        self, data: list[dict[str, str | float]], aggregate_field: str
    ) -> list[dict[str, float | int]]:
        """Вычисляет среднее значение по указанному полю."""

        super().check_items(data)
        result = []
        count = len(data)

        for field in data:
            super().check_type(field, aggregate_field)
            result.append(float(field[aggregate_field]))
        return [{"avg": round(sum(result) / count, 2)}]
