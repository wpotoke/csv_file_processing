from aggregators.base_aggregator import BaseAggregate


class AggregateMin(BaseAggregate):

    def aggregate(
        self, data: list[dict[str, str | float]], aggregate_field: str
    ) -> list[dict[str, float | int]]:
        """Вычисляет минимальное значение по указанному полю."""

        super().check_items(data)
        result = []
        count = len(data)

        for field in data:
            super().check_type(field, aggregate_field)
            result.append(float(field[aggregate_field]))
        return [{"min": min(result)}]
