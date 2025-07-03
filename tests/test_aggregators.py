from aggregators.avg_aggregator import AggregateAvg
from aggregators.max_aggregator import AggregateMax
from aggregators.min_aggregator import AggregateMin
from readers.csv_reader import CsvReader
import pytest


def test_aggregate_avg(sample_csv_file):
    data = CsvReader().read(sample_csv_file)
    avg = AggregateAvg().aggregate(data, "rating")[0]["avg"]
    assert isinstance(avg, float)
    assert round(avg, 1) == 4.5


def test_aggregate_min(sample_csv_file):
    data = CsvReader().read(sample_csv_file)
    result = AggregateMin().aggregate(data, "price")[0]["min"]
    assert result == 149.0


def test_aggregate_max(sample_csv_file):
    data = CsvReader().read(sample_csv_file)
    result = AggregateMax().aggregate(data, "price")[0]["max"]
    assert result == 1199.0


def test_aggregate_avg_single_entry():
    data = [{"price": "100"}]
    result = AggregateAvg().aggregate(data, "price")
    assert result == [{"avg": 100.0}]


def test_aggregate_min_typical_case():
    data = [{"price": "100"}, {"price": "50"}]
    result = AggregateMin().aggregate(data, "price")
    assert result == [{"min": 50.0}]


def test_aggregate_max_invalid_type():
    data = [{"price": "cheap"}, {"price": "expensive"}]
    with pytest.raises(TypeError):
        AggregateMax().aggregate(data, "price")
