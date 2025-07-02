from aggregators.base_aggregator import BaseAggregate


class AggregateAvg(BaseAggregate):

    def aggregate(
        self, data: list[dict[str, str | float]], aggregate_field: str
    ) -> list[dict[str, float | int]]:
        """Вычисляет среднее значение по указанному полю."""

        result = []
        count = len(data)

        for field in data:
            super().check_type(field, aggregate_field)
            result.append(float(field[aggregate_field]))
        return [{"avg": round(sum(result) / count, 2)}]
