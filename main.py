"""This module provides CLI commands using argparse and outputs results in table format."""
import argparse
import tabulate
import csv


# reader


def read(file_name):

    """without csv lib"""

    with open(file=file_name, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
        fieldnames = [field.strip() for field in lines[0].split(",")]
        data = [field.strip().split(",") for field in lines[1:]]

        print(fieldnames)
        print(data)

def read_csv(file_name):

    """with csv lib"""

    with open(file=file_name, mode="r", encoding="utf-8") as csvfile:
        reader = list(csv.reader(csvfile, delimiter=","))
        fieldnames = reader[0]
        data = reader[1:]

        print(fieldnames)
        print(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="file")
    args = parser.parse_args()
    file_name = args.file
    read_csv(file_name=file_name)
    print()
    read(file_name=file_name)
