from abc import ABC, abstractmethod
from ..types import SignSpec

class Renderer(ABC):
    @abstractmethod
    def render(self, spec: SignSpec, output_path: str):
        pass
