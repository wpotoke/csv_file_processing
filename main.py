"""This module provides CLI commands using argparse and outputs results in table format."""

import argparse
import csv
from abc import ABC, abstractmethod
from tabulate import tabulate


class BaseReader(ABC):

    @abstractmethod
    def read(self, file_name):
        pass


class BaseAggregate(ABC):

    @abstractmethod
    def aggregate(self, data, aggregate_field):
        pass


class BaseFilter(ABC):

    IS_DIGIT = False

    @abstractmethod
    def filter(self, data, filter_field, value):
        pass

    def determine_type(self, value):
        try:
            value = float(value)
            self.IS_DIGIT = True
        except (TypeError, ValueError):
            self.IS_DIGIT = False


class BasePrint(ABC):

    @abstractmethod
    def print(self, data):
        pass


class BaseOrderBy(ABC):

    @abstractmethod
    def order_by(self, data, field_order):
        pass


class CsvReader(BaseReader):

    def read(self, file_name):
        """reader with csv lib"""

        with open(file=file_name, mode="r", encoding="utf-8") as csvfile:
            reader = list(csv.reader(csvfile, delimiter=","))
            fieldnames = reader[0]
            data = reader[1:]

            data = [
                {fieldnames[j]: data[i][j] for j in range(len(fieldnames))}
                for i in range(len(data))
            ]

            return data


class FilterGT(BaseFilter):

    def filter(self, data, filter_field, value):
        result = []
        super().determine_type(value)
        if self.IS_DIGIT:
            for line in data:
                if float(line[filter_field]) > float(value):
                    result.append(line)
        if not self.IS_DIGIT:
            for line in data:
                if line[filter_field] > value:
                    result.append(line)
        return result


class FilterLT(BaseFilter):

    def filter(self, data, filter_field, value):
        result = []
        super().determine_type(value)
        if self.IS_DIGIT:
            for line in data:
                if float(line[filter_field]) < float(value):
                    result.append(line)
        if not self.IS_DIGIT:
            for line in data:
                if line[filter_field] < value:
                    result.append(line)
        return result


class FilterEq(BaseFilter):

    def filter(self, data, filter_field, value):
        result = []
        super().determine_type(value)
        if self.IS_DIGIT:
            for line in data:
                if float(line[filter_field]) == float(value):
                    result.append(line)
        if not self.IS_DIGIT:
            for line in data:
                if line[filter_field] == value:
                    result.append(line)
        return result


class AggregateAvg(BaseAggregate):

    def aggregate(self, data, aggregate_field):

        result = []
        count = len(data)

        for line in data:
            result.append(float(line[aggregate_field]))
        return [{"avg": round(sum(result) / count, 2)}]


class AggregateMin(BaseAggregate):

    def aggregate(self, data, aggregate_field):

        result = []
        count = len(data)

        for line in data:
            result.append(float(line[aggregate_field]))
        return [{"min": min(result)}]


class AggregateMax(BaseAggregate):

    def aggregate(self, data, aggregate_field):

        result = []
        count = len(data)

        for line in data:
            result.append(float(line[aggregate_field]))
        return [{"max": max(result)}]


class OrderByAsc(BaseOrderBy):

    def order_by(self, data, field_order):

        return sorted(data, key=lambda field: float(field[field_order]))


class OrderByDesc(BaseOrderBy):

    def order_by(self, data, field_order):

        return sorted(data, key=lambda field: float(field[field_order]), reverse=True)


class TablePrettyPrint(BasePrint):

    def print(self, data):
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

    allowed_filter_parameters = {
        ">": FilterGT,
        "<": FilterLT,
        "=": FilterEq
    }
    allowed_aggregate_values = {
        "avg": AggregateAvg,
        "min": AggregateMin,
        "max": AggregateMax,
    }
    allowed_order_by_parameters = {
        "asc": OrderByAsc,
        "desc": OrderByDesc
    }

    data = CsvReader().read(file_name)

    if filter_field is not None:
        for parameter in allowed_filter_parameters:
            if parameter in filter_field:
                filter_paremeter = parameter
                break
        else:
            pass
            # RAISE
        field, value = filter_field.split(filter_paremeter)
        data = allowed_filter_parameters[filter_paremeter]().filter(data, field, value)

    if aggregate_field is not None:
        field, type_aggregate = aggregate_field.split("=")
        data = allowed_aggregate_values[type_aggregate]().aggregate(data, field)

    if order_by_field is not None:
        field, order_by_paremeter = order_by_field.split("=")
        data = allowed_order_by_parameters[order_by_paremeter]().order_by(data, field)

    TablePrettyPrint().print(data)
