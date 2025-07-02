from abc import ABC, abstractmethod


class BaseAggregate(ABC):

    @abstractmethod
    def aggregate(
        self, data: list[dict[str, str | float]], aggregate_field: str
    ) -> list[dict[str, str | float]]:
        """Выполняет агрегацию данных по заданному полю."""

    def check_type(self, field: dict[str, str | float], field_aggregate: str) -> None:
        """Проверяет, можно ли преобразовать значение поля к числу."""
        try:
            float(field[field_aggregate])
        except ValueError:
            raise TypeError(f"Cannot sort by non-numeric field '{field_aggregate}'.")
