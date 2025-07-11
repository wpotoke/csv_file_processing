import argparse


# === Базовое исключение проекта ===


class CSVProcessingError(Exception):
    """Базовое исключение для всех пользовательских ошибок при обработке CSV."""


# === Исключения по типам операций ===


class EmptyCSVError(CSVProcessingError):
    """CSV-файл пустой или не содержит данных."""


class UnsupportedFilterOperatorError(CSVProcessingError):
    """Использован неподдерживаемый оператор фильтрации."""


class UnsupportedAggregateError(CSVProcessingError):
    """Использован неподдерживаемый тип агрегации."""


class UnsupportedOrderByError(CSVProcessingError):
    """Использован неподдерживаемый тип сортировки."""


# === Кастомный ArgumentParser для CLI ===


class CustomArgumentParser(argparse.ArgumentParser):
    """Кастомный парсер, переопределен метод error для отлова ошибки"""

    def error(self, message):
        try:
            raise ValueError("Error paremeters")
        except ValueError as e:
            print(e)
            print(message)
            print(self.print_help())
            exit(1)
