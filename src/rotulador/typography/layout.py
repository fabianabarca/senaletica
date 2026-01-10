"""
Motor de layout para texto avanzado.
Maneja wrapping, line-height, y posicionamiento.
"""

from typing import List, Tuple
import cairo
from .metrics import TextMetrics

class LayoutEngine:
    """
    Motor para layout de texto con wrapping automático y control de línea.
    """
    
    def __init__(self, ctx: cairo.Context, font_family: str = "Myriad Pro", font_size: float = 12.0, line_height: float = 1.2):
        self.ctx = ctx
        self.font_family = font_family
        self.font_size = font_size
        self.line_height = line_height
        self._setup_font()
    
    def _setup_font(self):
        """Configura la fuente en el contexto Cairo."""
        from ..typography.loader import FontLoader
        FontLoader.load_font(self.ctx, self.font_family)
        self.ctx.set_font_size(self.font_size)
    
    def wrap_text(self, text: str, max_width: float) -> List[str]:
        """
        Parte el texto en líneas que quepan dentro de max_width.
        Retorna lista de líneas.
        """
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            # Probar agregar la palabra a la línea actual
            test_line = current_line + " " + word if current_line else word
            test_width = self.ctx.text_extents(test_line).width
            
            if test_width <= max_width:
                current_line = test_line
            else:
                # La palabra no cabe, guardar línea actual y empezar nueva
                if current_line:
                    lines.append(current_line)
                current_line = word
                
                # Si una sola palabra es más ancha que max_width, truncar o dividir (simple: truncar)
                if self.ctx.text_extents(word).width > max_width:
                    # Para MVP, truncar con "..."
                    truncated = word
                    while self.ctx.text_extents(truncated + "...").width > max_width and len(truncated) > 0:
                        truncated = truncated[:-1]
                    current_line = truncated + "..." if truncated else "..."
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def get_text_height(self, lines: List[str]) -> float:
        """
        Calcula la altura total de un bloque de texto multilínea.
        """
        if not lines:
            return 0
        line_height_px = self.font_size * self.line_height
        return len(lines) * line_height_px
    
    def draw_multiline_text(self, lines: List[str], x: float, y: float, color: Tuple[float, float, float], align: str = "left"):
        """
        Dibuja texto multilínea.
        y es la posición de la primera línea (baseline).
        """
        self.ctx.set_source_rgb(*color)
        line_height_px = self.font_size * self.line_height
        
        for i, line in enumerate(lines):
            line_y = y + i * line_height_px
            
            # Calcular offset X según alineación
            if align == "center":
                line_width = self.ctx.text_extents(line).width
                draw_x = x - line_width / 2
            elif align == "right":
                line_width = self.ctx.text_extents(line).width
                draw_x = x - line_width
            else:  # left
                draw_x = x
            
            self.ctx.move_to(draw_x, line_y)
            self.ctx.show_text(line)