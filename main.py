"""This module provides CLI commands using argparse"""

from exceptions import CustomArgumentParser
from reader.csv_reader import CsvReader
from operations.orders import OrderByAsc, OrderByDesc
from operations.filters import FilterEq, FilterGT, FilterLT
from operations.aggregators import AggregateAvg, AggregateMax, AggregateMin
from printer.table_printer import TablePrettyPrint


def main():
    parser = CustomArgumentParser()

    parser.add_argument("--file", type=str, required=True, help="Path to CSV file")
    parser.add_argument("--where", default=None, type=str, help="Filtering condition")
    parser.add_argument(
        "--aggregate", default=None, type=str, help="Aggregation operation"
    )
    parser.add_argument("--order_by", default=None, type=str, help="Sorting order")

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
    last_operation = None

    if filter_field is not None:
        for parameter in allowed_filter_parameters:
            if parameter in filter_field:
                filter_parameter = parameter
                break
        else:
            raise ValueError(
                f"Unsupported filter condition in '{filter_field}'. "
                f"Allowed: {list(allowed_filter_parameters.keys())}"
            )

        field, value = filter_field.split(filter_parameter)
        operation = allowed_filter_parameters[filter_parameter]()
        data = operation.filter(data, field, value)
        last_operation = operation

    if aggregate_field is not None:
        field, type_aggregate = aggregate_field.split("=")
        if type_aggregate not in allowed_aggregate_values:
            raise ValueError(
                f"Unsupported aggregate type '{type_aggregate}'. "
                f"Allowed: {list(allowed_aggregate_values.keys())}"
            )
        operation = allowed_aggregate_values[type_aggregate]()
        data = operation.aggregate(data, field)
        last_operation = operation

    if order_by_field is not None:
        field, order_by_parameter = order_by_field.split("=")
        if order_by_parameter not in allowed_order_by_parameters:
            raise ValueError(
                f"Unsupported order_by type '{order_by_parameter}'. "
                f"Allowed: {list(allowed_order_by_parameters.keys())}"
            )
        operation = allowed_order_by_parameters[order_by_parameter]()
        data = operation.order_by(data, field)
        last_operation = operation

    if last_operation is not None:
        last_operation.print(data)
    else:
        TablePrettyPrint().print(data)


if __name__ == "__main__":
    main()
