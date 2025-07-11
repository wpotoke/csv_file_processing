import pytest
from printer.table_printer import TablePrettyPrint


def test_pretty_print_empty_data():
    with pytest.raises(ValueError):
        TablePrettyPrint().print([])


def test_table_pretty_print_output(capsys):
    printer = TablePrettyPrint()
    data = [{"name": "test", "price": 100, "rating": 4.5}]
    printer.print(data)
    captured = capsys.readouterr()
    assert "test" in captured.out
    assert "100" in captured.out
