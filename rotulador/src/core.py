from typing import Optional, List
from .types import SignSpec, SignType
from .templates.vertical import VerticalPostTemplate
from .renderers.cairo import CairoRenderer

class Rotulo:
    """Main entry point for generating signs."""
    
    def __init__(self):
        self.renderer = CairoRenderer()

    def create_spec(self, sign_type: SignType, stop_name: str) -> SignSpec:
        """
        Factory method to create a Sign Specification based on type and input.
        This is where the 'Design Intelligence' lives (via Templates).
        """
        if sign_type == SignType.VERTICAL:
            template = VerticalPostTemplate()
            return template.generate_spec(stop_name)
        else:
            raise NotImplementedError(f"Sign type {sign_type} not implemented yet.")

    def render(self, spec: SignSpec, output_path: str):
        """Passthrough to renderer."""
        self.renderer.render(spec, output_path)
    
    def generate(self, sign_type: SignType, stop_name: str, output_path: str):
        """Helper to do it all at once."""
        spec = self.create_spec(sign_type, stop_name)
        self.render(spec, output_path)
