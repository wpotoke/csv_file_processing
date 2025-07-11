from abc import ABC, abstractmethod
from typing import Callable, Union
from mixins.mixin_eror.no_data_mixin import NoDataMixin
from printer.table_printer import TablePrettyPrint


class BaseFilter(TablePrettyPrint, ABC, NoDataMixin):
    IS_DIGIT: bool = False

    @abstractmethod
    def filter(
        self, data: list[dict[str, str | float]], filter_field: str, value: str
    ) -> list[dict[str, str | float]]:
        """Фильтрует данные по значению поля."""

    def determine_type(self, value: str) -> None:
        try:
            float(value)
            self.IS_DIGIT = True
        except (TypeError, ValueError):
            self.IS_DIGIT = False

    def _apply_condition(
        self,
        data: list[dict[str, str | float]],
        field: str,
        value: Union[str, float],
        op: Callable[[Union[str, float], Union[str, float]], bool],
    ) -> list[dict[str, str | float]]:
        result = []
        for line in data:
            if op(line[field], value):
                result.append(line)
        return result


class FilterEq(BaseFilter):
    def filter(
        self, data: list[dict[str, str | float]], filter_field: str, value: str
    ) -> list[dict[str, str | float]]:
        """Фильтрует строки, где значение поля равно заданному."""

        super().determine_type(value)
        super().check_items(data)
        if self.IS_DIGIT:
            return self._apply_condition(
                data, filter_field, float(value), lambda x, y: float(x) == float(y)
            )
        if not self.IS_DIGIT:
            return self._apply_condition(
                data, filter_field, value, lambda x, y: str(x) == str(y)
            )


class FilterGT(BaseFilter):
    def filter(
        self, data: list[dict[str, str | float]], filter_field: str, value: str
    ) -> list[dict[str, str | float]]:
        """Фильтрует строки, где значение поля больше заданного."""

        super().determine_type(value)
        super().check_items(data)
        if self.IS_DIGIT:
            return self._apply_condition(
                data, filter_field, float(value), lambda x, y: float(x) > float(y)
            )
        if not self.IS_DIGIT:
            return self._apply_condition(
                data, filter_field, value, lambda x, y: str(x) > str(y)
            )


class FilterLT(BaseFilter):
    def filter(
        self, data: list[dict[str, str | float]], filter_field: str, value: str
    ) -> list[dict[str, str | float]]:
        """Фильтрует строки, где значение поля меньше заданного."""

        super().determine_type(value)
        super().check_items(data)
        if self.IS_DIGIT:
            return self._apply_condition(
                data, filter_field, float(value), lambda x, y: float(x) < float(y)
            )
        if not self.IS_DIGIT:
            return self._apply_condition(
                data, filter_field, value, lambda x, y: str(x) < str(y)
            )
