from readers.csv_reader import CsvReader 

def test_csv_reader_reads_correctly(sample_csv_file):
    data = CsvReader().read(sample_csv_file)
    assert isinstance(data, list)
    assert len(data) == 10
    assert data[0]["name"] == "iphone 15 pro"
    assert data[1]["price"] == "1199"
