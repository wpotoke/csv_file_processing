import pytest

from operations.orders import OrderByAsc, OrderByDesc
from reader.csv_reader import CsvReader


def test_order_by_asc(sample_csv_file):
    data = CsvReader().read(sample_csv_file)
    result = OrderByAsc().order_by(data, "price")
    prices = [float(row["price"]) for row in result]
    assert prices == sorted(prices)


def test_order_by_desc(sample_csv_file):
    data = CsvReader().read(sample_csv_file)
    result = OrderByDesc().order_by(data, "price")
    prices = [float(row["price"]) for row in result]
    assert prices == sorted(prices, reverse=True)


def test_order_by_asc_valid():
    data = [{"rating": "3.0"}, {"rating": "1.0"}, {"rating": "5.0"}]
    result = OrderByAsc().order_by(data, "rating")
    assert [r["rating"] for r in result] == ["1.0", "3.0", "5.0"]


def test_order_by_desc_invalid_type():
    data = [{"rating": "high"}, {"rating": "low"}]
    with pytest.raises(TypeError):
        OrderByDesc().order_by(data, "rating")
