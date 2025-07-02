"""This module provides CLI commands using argparse and outputs results in table format."""

import argparse
import tabulate
import csv


def read_csv(file_name):
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


def filter(data, filter_field):
    allowed_operators = ["<", ">", "="]
    is_digit = False

    index_operator = [
        filter_field.find(oper) for oper in allowed_operators if oper in filter_field
    ][0]
    operator = filter_field[index_operator]
    field, value = filter_field.split(operator)

    try:
        value = float(value)
        is_digit = True
    except TypeError:
        value = str(value)

    result = []
    for line in data:
        if is_digit:
            if operator == "<":
                if float(line[field]) < value:
                    result.append(line)
            if operator == ">":
                if float(line[field]) > value:
                    result.append(line)
            if operator == "=":
                if float(line[field]) == value:
                    result.append(line)
        else:
            if operator == "<":
                if line[field] < value:
                    result.append(line)
            if operator == ">":
                if line[field] > value:
                    result.append(line)
            if operator == "=":
                if line[field] == value:
                    result.append(line)
    return result


def aggregate(aggregate_field):
    print(aggregate_field)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", type=str, required=True, help="file")
    parser.add_argument("--where", default=None, type=str, help="filter")
    parser.add_argument("--aggregate", default=None, type=str, help="aggregate")

    args = parser.parse_args()

    file_name = args.file
    filter_field = args.where
    aggregate_field = args.aggregate

    data = read_csv(file_name=file_name)
    if filter_field is not None:
        filter(data=data, filter_field=filter_field)
    if aggregate_field is not None:
        aggregate(aggregate_field=aggregate_field)
