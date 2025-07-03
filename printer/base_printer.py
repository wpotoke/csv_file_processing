from abc import ABC, abstractmethod
from mixins.mixin_eror.no_data_mixin import NoDataMixin


class BasePrint(ABC, NoDataMixin):

    @abstractmethod
    def print(self, data: list[dict[str, str | float]]) -> None:
        """Выводит данные в консоль."""
