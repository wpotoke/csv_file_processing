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

