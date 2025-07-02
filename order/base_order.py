from abc import ABC, abstractmethod


class BaseOrderBy(ABC):

    def check_type(self, field: dict[str, str | float], field_order: str) -> None:
        try:
            float(field[field_order])
        except ValueError:
            raise TypeError(f"Cannot sort by non-numeric field '{field_order}'.")

    @abstractmethod
    def order_by(self, data, field_order) -> list[dict[str, str | float]]:
        """Сортирует данные по указанному полю."""
