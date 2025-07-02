import csv

from typing import Any, Callable
from readers.base_reader import BaseReader

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