from filters.base_filter import BaseFilter


class FilterEq(BaseFilter):

    def filter(
        self, data: list[dict[str, str]], filter_field: str, value: str
    ) -> list[dict[str, str]]:
        """Фильтрует строки, где значение поля равно заданному."""

        super().determine_type(value)
        super().check_items(data)
        if self.IS_DIGIT:
            return self._apply_condition(
                data, filter_field, float(value), lambda x, y: float(x) == y
            )
        if not self.IS_DIGIT:
            return self._apply_condition(data, filter_field, value, lambda x, y: x == y)
