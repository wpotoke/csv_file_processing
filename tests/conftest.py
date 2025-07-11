import tempfile
import pytest

CSV_CONTENT = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
iphone 14,apple,799,4.7
galaxy a54,samsung,349,4.2
poco x5 pro,xiaomi,299,4.4
iphone se,apple,429,4.1
galaxy z flip 5,samsung,999,4.6
redmi 10c,xiaomi,149,4.1
iphone 13 mini,apple,599,4.5
"""


@pytest.fixture
def sample_csv_file():
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False) as f:
        f.write(CSV_CONTENT)
        f.seek(0)
        yield f.name
