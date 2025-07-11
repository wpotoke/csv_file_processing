from operations.filters import FilterEq, FilterGT, FilterLT
from operations.aggregators import AggregateAvg, AggregateMin, AggregateMax
from operations.orders import OrderByAsc, OrderByDesc

DATA = [
    {"name": "iphone", "price": "999", "rating": "4.9"},
    {"name": "galaxy", "price": "799", "rating": "4.5"},
    {"name": "redmi", "price": "199", "rating": "4.2"},
    {"name": "poco", "price": "299", "rating": "4.4"},
]


def test_filter_gt_and_aggregate_avg():
    filtered = FilterGT().filter(DATA, "price", "200")
    result = AggregateAvg().aggregate(filtered, "price")
    assert result == [{"avg": 699.0}]


def test_filter_lt_and_aggregate_min():
    filtered = FilterLT().filter(DATA, "price", "800")
    result = AggregateMin().aggregate(filtered, "price")
    assert result == [{"min": 199.0}]


def test_filter_eq_and_aggregate_max():
    filtered = FilterEq().filter(DATA, "rating", "4.9")
    result = AggregateMax().aggregate(filtered, "rating")
    assert result == [{"max": 4.9}]


def test_filter_gt_and_order_by_asc():
    filtered = FilterGT().filter(DATA, "price", "200")
    result = OrderByAsc().order_by(filtered, "rating")
    assert [r["name"] for r in result] == ["poco", "galaxy", "iphone"]


def test_filter_lt_and_order_by_desc():
    filtered = FilterLT().filter(DATA, "price", "800")
    result = OrderByDesc().order_by(filtered, "price")
    assert [r["name"] for r in result] == ["galaxy", "poco", "redmi"]


def test_order_by_asc_and_aggregate_max():
    ordered = OrderByAsc().order_by(DATA, "price")
    result = AggregateMax().aggregate(ordered, "rating")
    assert result == [{"max": 4.9}]


def test_order_by_desc_and_aggregate_min():
    ordered = OrderByDesc().order_by(DATA, "rating")
    result = AggregateMin().aggregate(ordered, "price")
    assert result == [{"min": 199.0}]


def test_chain_gt_avg_order():
    filtered = FilterGT().filter(DATA, "price", "200")
    aggregated = AggregateAvg().aggregate(filtered, "price")
    ordered = OrderByAsc().order_by(filtered, "price")
    assert aggregated == [{"avg": 699.0}]
    assert [r["name"] for r in ordered] == ["poco", "galaxy", "iphone"]


def test_chain_lt_max_order():
    filtered = FilterLT().filter(DATA, "price", "800")
    aggregated = AggregateMax().aggregate(filtered, "price")
    ordered = OrderByDesc().order_by(filtered, "rating")
    assert aggregated == [{"max": 799.0}]
    assert [r["name"] for r in ordered] == ["galaxy", "poco", "redmi"]


def test_chain_eq_min_order():
    filtered = FilterEq().filter(DATA, "name", "iphone")
    aggregated = AggregateMin().aggregate(filtered, "rating")
    ordered = OrderByAsc().order_by(filtered, "price")
    assert aggregated == [{"min": 4.9}]
    assert ordered == [{"name": "iphone", "price": "999", "rating": "4.9"}]


def test_filter_gt_then_aggregate_avg():
    data = [
        {"price": "100"},
        {"price": "200"},
        {"price": "50"},
    ]
    filtered = FilterGT().filter(data, "price", "99")
    result = AggregateAvg().aggregate(filtered, "price")
    assert result == [{"avg": 150.0}]


def test_filter_gt_aggregate_min():
    data = [
        {"rating": "4.9"},
        {"rating": "4.6"},
        {"rating": "4.1"},
    ]
    filtered = FilterGT().filter(data, "rating", "4.1")
    result = AggregateMin().aggregate(filtered, "rating")
    assert result == [{"min": 4.6}]
