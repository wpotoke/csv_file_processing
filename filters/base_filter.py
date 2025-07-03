from abc import ABC, abstractmethod
from typing import Callable
from mixins.mixin_eror.no_data_mixin import NoDataMixin

class BaseFilter(ABC, NoDataMixin):

    IS_DIGIT = False

    @abstractmethod
    def filter(
        self, data: list[dict[str, str]], filter_field: str, value: str
    ) -> list[dict[str, str | float]]:
        """Фильтрует данные по значению поля."""

    def determine_type(self, value: str) -> None:
        """Применяет условие фильтрации к каждому элементу данных."""
        try:
            value = float(value)
            self.IS_DIGIT = True
        except (TypeError, ValueError):
            self.IS_DIGIT = False

    def _apply_condition(
        self,
        data: list[dict[str, str]],
        field: str,
        value: str | int,
        op: Callable[[str, str | float], bool],
    ) -> list[dict[str, str]]:
        result = []
        for line in data:
            if op(line[field], value):
                result.append(line)
        return result
