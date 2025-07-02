"""This module provides CLI commands using argparse and outputs results in table format."""

import argparse
import csv
from abc import ABC, abstractmethod
from tabulate import tabulate


class BaseReader(ABC):
    
    @abstractmethod
    def read(self, file_name):
        pass


class Aggregate(ABC):

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


class Print(ABC):

    @abstractmethod
    def print(self, data):
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
        self.determine_type(value)
        if self.IS_DIGIT:
            for line in data:
                if float(line[filter_field]) > value:
                    result.append(line)
        if not self.IS_DIGIT:
            for line in data:
                if line[filter_field] > value:
                    result.append(line)
        return result


class FilterLT(BaseFilter):

    def filter(self, data, filter_field, value):
        result = []
        self.determine_type(value)
        if self.IS_DIGIT:
            for line in data:
                if float(line[filter_field]) < value:
                    result.append(line)
        if not self.IS_DIGIT:
            for line in data:
                if line[filter_field] < value:
                    result.append(line)
        return result


class FilterEq(BaseFilter):

    def filter(self, data, filter_field, value):
        result = []
        self.determine_type(value)
        if self.IS_DIGIT:
            for line in data:
                if float(line[filter_field]) == value:
                    result.append(line)
        if not self.IS_DIGIT:
            for line in data:
                if line[filter_field] == value:
                    result.append(line)
        return result


class AggregateAvg(Aggregate):

    def aggregate(self, data, aggregate_field):
        aggr_field = aggregate_field.split("=")[0]

        result = []
        count = len(data)

        for line in data:
            result.append(float(line[aggr_field]))
        return [{"avg": round(sum(result) / count, 2)}]


class AggregateMin(Aggregate):

    def aggregate(self, data, aggregate_field):
        aggr_field = aggregate_field.split("=")[0]

        result = []
        count = len(data)

        for line in data:
            result.append(float(line[aggr_field]))
        return [{"min": min(result)}]


class AggregateMax(Aggregate):

    def aggregate(self, data, aggregate_field):
        aggr_field = aggregate_field.split("=")[0]

        result = []
        count = len(data)

        for line in data:
            result.append(float(line[aggr_field]))
        return [{"max": max(result)}]


class TablePrettyPrint(Print):

    def pretty_print(self, data):
        table = [field.values() for field in data]
        headers = [i for i in data[0]]
        print(tabulate(table, headers, tablefmt="pretty"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", type=str, required=True, help="file")
    parser.add_argument("--where", default=None, type=str, help="filter")
    parser.add_argument("--aggregate", default=None, type=str, help="aggregate")

    args = parser.parse_args()

    file_name = args.file
    filter_field = args.where
    aggregate_field = args.aggregate

    # data = read(file_name=file_name)
    # if filter_field is not None:
    #     data = filter(data=data, filter_field=filter_field)
    # if aggregate_field is not None:
    #     data = aggregate(data=data, aggregate_field=aggregate_field)
    # pretty_print(data)
