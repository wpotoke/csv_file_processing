from filters.gt_filter import FilterGT
from filters.lt_filter import FilterLT
from filters.eq_filter import FilterEq
from readers.csv_reader import CsvReader

DATA = [
    {"name": "item1", "price": "100"},
    {"name": "item2", "price": "200"},
    {"name": "item3", "price": "300"},
]


def test_filter_eq_no_match():
    result = FilterEq().filter(DATA, "price", "999")
    assert result == []


def test_filter_gt_text_comparison():
    data = [{"name": "A"}, {"name": "Z"}]
    result = FilterGT().filter(data, "name", "B")
    assert result == [{"name": "Z"}]


