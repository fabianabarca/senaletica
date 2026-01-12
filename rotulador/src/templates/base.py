from abc import ABC, abstractmethod
from ..types import SignSpec

class Template(ABC):
    @abstractmethod
    def generate_spec(self, stop_name: str) -> SignSpec:
        pass
