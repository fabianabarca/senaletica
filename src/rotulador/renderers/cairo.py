import cairo
import math
from ..renderers.base import Renderer
from ..typography.loader import FontLoader
from ..typography.metrics import TextMetrics

class CairoRenderer(Renderer):
    """
    Renderizador basado en pycairo.
    """
    
    def __init__(self):
        self.surface = None
        self.ctx = None
        self.width = 0
        self.height = 0
        
    def setup(self, width: int, height: int):
        self.width = width
        self.height = height
        self.surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(0, 0, width, height))
        self.ctx = cairo.Context(self.surface)
        
    def draw_background(self, color: tuple):
        self.ctx.set_source_rgb(*color)
        self.ctx.paint()

    def draw_circle(self, x: float, y: float, radius: float, color: tuple):
        self.ctx.arc(x, y, radius, 0, 2 * math.pi)
        self.ctx.set_source_rgb(*color)
        self.ctx.fill()
        
    def draw_text(self, text: str, x: float, y: float, font_size: float, 
                  color: tuple, font_family: str = "Myriad Pro", align: str = "left"):
        
        FontLoader.load_font(self.ctx, font_family)
        self.ctx.set_font_size(font_size)
        self.ctx.set_source_rgb(*color)
        
        metrics = TextMetrics(self.ctx, text)
        
        draw_x = x
        draw_y = y
        
        if align == "center":
            draw_x += metrics.center_offset_x
            draw_y += metrics.center_offset_y
        elif align == "left":
            # Cairo dibuja desde el baseline. Ajuste simple si y es "top" o "baseline"
            # Asumiremos y es baseline por defecto en cairo
            pass
            
        self.ctx.move_to(draw_x, draw_y)
        self.ctx.show_text(text)

    def get_text_width(self, text: str, font_family: str, font_size: float) -> float:
        FontLoader.load_font(self.ctx, font_family)
        self.ctx.set_font_size(font_size)
        metrics = TextMetrics(self.ctx, text)
        return metrics.width
        
    def save(self, filename: str):
        if filename.endswith(".svg"):
            surface = cairo.SVGSurface(filename, self.width, self.height)
        elif filename.endswith(".png"):
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(self.width), int(self.height))
        elif filename.endswith(".pdf"):
            surface = cairo.PDFSurface(filename, self.width, self.height)
        else:
            raise ValueError("Formato no soportado. Use .svg, .png o .pdf")
            
        # Replay recording surface to destination
        ctx = cairo.Context(surface)
        ctx.set_source_surface(self.surface, 0, 0)
        ctx.paint()
        
        if filename.endswith(".png"):
            surface.write_to_png(filename)
            
        surface.finish()
