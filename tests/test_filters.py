from operations.filters import FilterGT, FilterLT, FilterEq
from reader.csv_reader import CsvReader

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


def test_filter_lt_numeric():
    result = FilterLT().filter(DATA, "price", "250")
    assert len(result) == 2


def test_filter_gt(sample_csv_file):
    data = CsvReader().read(sample_csv_file)
    result = FilterGT().filter(data, "price", "1000")
    assert all(float(item["price"]) > 1000 for item in result)


def test_filter_lt(sample_csv_file):
    data = CsvReader().read(sample_csv_file)
    result = FilterLT().filter(data, "rating", "4.3")
    assert all(float(item["rating"]) < 4.3 for item in result)


def test_filter_eq(sample_csv_file):
    data = CsvReader().read(sample_csv_file)
    result = FilterEq().filter(data, "brand", "apple")
    assert all(item["brand"] == "apple" for item in result)
