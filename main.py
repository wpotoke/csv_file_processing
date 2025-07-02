"""This module provides CLI commands using argparse"""

import argparse

from readers.csv_reader import CsvReader
from filters.eq_filter import FilterEq
from filters.gt_filter import FilterGT
from filters.lt_filter import FilterLT
from aggregators.avg_aggregator import AggregateAvg
from aggregators.max_aggregator import AggregateMax
from aggregators.min_aggregator import AggregateMin
from order.asc_order import OrderByAsc
from order.desc_order import OrderByDesc
from printer.table_pretty_printer import TablePrettyPrint


def main():
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


if __name__ == "__main__":
    main()
