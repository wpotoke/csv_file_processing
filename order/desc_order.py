from order.base_order import BaseOrderBy


class OrderByDesc(BaseOrderBy):

    def order_by(
        self, data: list[dict[str, str | float]], field_order: str
    ) -> list[dict[str, str | float]]:
        """Сортирует данные по убыванию по указанному полю."""

        for field in data:
            super().check_type(field, field_order)
        return sorted(data, key=lambda field: float(field[field_order]), reverse=True)
