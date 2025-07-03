class NoDataMixin:
    def check_items(self, data: list[dict[str, str | float]]) -> None:
        if not data:
            raise ValueError(
                "No data: the data object is empty. Check your params of filter or order or file"
            )
