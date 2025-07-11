import csv

from abc import ABC, abstractmethod


class BaseReader(ABC):
    @abstractmethod
    def read(self, file_name: str) -> list[dict[str, str]]:
        """Читает данные из файла и возвращает список словарей."""


class CsvReader(BaseReader):
    def read(self, file_name: str) -> list[dict[str, str]]:
        """Читает CSV-файл и возвращает список словарей."""

        with open(file=file_name, mode="r", encoding="utf-8") as csvfile:
            reader = list(csv.reader(csvfile, delimiter=","))
            if not reader:
                raise ValueError("The provided CSV file is empty.")
            fieldnames = reader[0]
            row = reader[1:]

            result = [
                {fieldnames[j]: row[i][j] for j in range(len(fieldnames))}
                for i in range(len(row))
            ]

            return result
