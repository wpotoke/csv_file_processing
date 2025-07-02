"""This module provides CLI commands using argparse and outputs results in table format."""

import argparse
import csv
from typing import Any, Callable
from abc import ABC, abstractmethod
from tabulate import tabulate


class BaseReader(ABC):

    @abstractmethod
    def read(self, file_name: str) -> list[dict[str, str]]:
        """Читает данные из файла и возвращает список словарей."""


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


class BaseFilter(ABC):

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


class BasePrint(ABC):

    @abstractmethod
    def print(self, data: list[dict[str, str | float]]) -> None:
        """Выводит данные в консоль."""


class BaseOrderBy(ABC):

    def check_type(self, field: dict[str, str | float], field_order: str) -> None:
        try:
            float(field[field_order])
        except ValueError:
            raise TypeError(f"Cannot sort by non-numeric field '{field_order}'.")

    @abstractmethod
    def order_by(self, data, field_order) -> list[dict[str, str | float]]:
        """Сортирует данные по указанному полю."""


class CsvReader(BaseReader):

    def read(self, file_name: str) -> list[dict[str, str]]:
        """Читает CSV-файл и возвращает список словарей."""

        with open(file=file_name, mode="r", encoding="utf-8") as csvfile:
            reader = list(csv.reader(csvfile, delimiter=","))
            if not reader:
                raise ValueError("The provided CSV file is empty.")
            fieldnames = reader[0]
            data = reader[1:]

            data = [
                {fieldnames[j]: data[i][j] for j in range(len(fieldnames))}
                for i in range(len(data))
            ]

            return data


class FilterGT(BaseFilter):

    def filter(
        self, data: list[dict[str, str]], filter_field: str, value: str
    ) -> list[dict[str, str]]:
        """Фильтрует строки, где значение поля больше заданного."""

        super().determine_type(value)
        if self.IS_DIGIT:
            return self._apply_condition(
                data, filter_field, float(value), lambda x, y: float(x) > y
            )
        if not self.IS_DIGIT:
            return self._apply_condition(data, filter_field, value, lambda x, y: x > y)


class FilterLT(BaseFilter):

    def filter(
        self, data: list[dict[str, str]], filter_field: str, value: str
    ) -> list[dict[str, str]]:
        """Фильтрует строки, где значение поля меньше заданного."""

        super().determine_type(value)
        if self.IS_DIGIT:
            return self._apply_condition(
                data, filter_field, float(value), lambda x, y: float(x) < y
            )
        if not self.IS_DIGIT:
            return self._apply_condition(data, filter_field, value, lambda x, y: x < y)


class FilterEq(BaseFilter):

    def filter(
        self, data: list[dict[str, str]], filter_field: str, value: str
    ) -> list[dict[str, str]]:
        """Фильтрует строки, где значение поля равно заданному."""

        super().determine_type(value)
        if self.IS_DIGIT:
            return self._apply_condition(
                data, filter_field, float(value), lambda x, y: float(x) == y
            )
        if not self.IS_DIGIT:
            return self._apply_condition(data, filter_field, value, lambda x, y: x == y)


class AggregateAvg(BaseAggregate):

    def aggregate(
        self, data: list[dict[str, str | float]], aggregate_field: str
    ) -> list[dict[str, float | int]]:
        """Вычисляет среднее значение по указанному полю."""

        result = []
        count = len(data)

        for field in data:
            super().check_type(field, aggregate_field)
            result.append(float(field[aggregate_field]))
        return [{"avg": round(sum(result) / count, 2)}]


class AggregateMin(BaseAggregate):

    def aggregate(
        self, data: list[dict[str, str | float]], aggregate_field: str
    ) -> list[dict[str, float | int]]:
        """Вычисляет минимальное значение по указанному полю."""

        result = []
        count = len(data)

        for field in data:
            super().check_type(field, aggregate_field)
            result.append(float(field[aggregate_field]))
        return [{"min": min(result)}]


class AggregateMax(BaseAggregate):

    def aggregate(
        self, data: list[dict[str, str | float]], aggregate_field: str
    ) -> list[dict[str, float | int]]:
        """Вычисляет максимальное значение по указанному полю."""

        result = []
        count = len(data)

        for field in data:
            super().check_type(field, aggregate_field)
            result.append(float(field[aggregate_field]))
        return [{"max": max(result)}]


class OrderByAsc(BaseOrderBy):

    def order_by(
        self, data: list[dict[str, str | float]], field_order: str
    ) -> list[dict[str, str | float]]:
        """Сортирует данные по возрастанию по указанному полю."""

        for field in data:
            super().check_type(field, field_order)
        return sorted(data, key=lambda field: float(field[field_order]))


class OrderByDesc(BaseOrderBy):

    def order_by(
        self, data: list[dict[str, str | float]], field_order: str
    ) -> list[dict[str, str | float]]:
        """Сортирует данные по убыванию по указанному полю."""

        for field in data:
            super().check_type(field, field_order)
        return sorted(data, key=lambda field: float(field[field_order]), reverse=True)


class TablePrettyPrint(BasePrint):

    def print(self, data: list[dict[str, str | float | int]]) -> None:
        """Выводит данные в виде таблицы."""

        table = [field.values() for field in data]
        headers = [i for i in data[0]]
        print(tabulate(table, headers, tablefmt="pretty"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", type=str, required=True, help="file")
    parser.add_argument("--where", default=None, type=str, help="filter")
    parser.add_argument("--aggregate", default=None, type=str, help="aggregate")
    parser.add_argument("--order_by", default=None, type=str, help="order_by")

    args = parser.parse_args()

    file_name = args.file
    filter_field = args.where
    aggregate_field = args.aggregate
    order_by_field = args.order_by

    allowed_filter_parameters = {">": FilterGT, "<": FilterLT, "=": FilterEq}
    allowed_aggregate_values = {
        "avg": AggregateAvg,
        "min": AggregateMin,
        "max": AggregateMax,
    }
    allowed_order_by_parameters = {"asc": OrderByAsc, "desc": OrderByDesc}

    data = CsvReader().read(file_name)

    if filter_field is not None:
        for parameter in allowed_filter_parameters:
            if parameter in filter_field:
                filter_parameter = parameter
                break
        else:
            raise ValueError(
                f"Unsupported filter condition in '{filter_field}'. Allowed: {list(allowed_filter_parameters)}"
            )

        field, value = filter_field.split(filter_parameter)
        data = allowed_filter_parameters[filter_parameter]().filter(data, field, value)

    if aggregate_field is not None:
        field, type_aggregate = aggregate_field.split("=")
        data = allowed_aggregate_values[type_aggregate]().aggregate(data, field)
    if type_aggregate not in allowed_aggregate_values:
        raise ValueError(
            f"Unsupported aggregate type '{type_aggregate}'. Allowed: {list(allowed_aggregate_values)}"
        )

    if order_by_field is not None:
        field, order_by_parameter = order_by_field.split("=")
        data = allowed_order_by_parameters[order_by_parameter]().order_by(data, field)

    TablePrettyPrint().print(data)
