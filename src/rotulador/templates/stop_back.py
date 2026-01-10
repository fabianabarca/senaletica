from .base import SignTemplate
from ..styles.colors import Colors
from ..styles.dimensions import Dimensions
from ..utils.conversion import mm_to_pt
from ..typography.layout import LayoutEngine
from ..models import StopData

class StopBackTemplate(SignTemplate):
    """
    Plantilla para rótulo de respaldo (Stop Back).
    Diseño: Círculo azul con 'b' blanca + Nombre de parada.
    """
    
    def render(self, stop_data: StopData):
        # 1. Setup canvas
        self.renderer.setup(Dimensions.get_default_width_pt(), Dimensions.get_default_height_pt())
        
        # 2. Background (Blanco)
        self.renderer.draw_background(Colors.WHITE)
        
        # 3. Círculo Azul
        self.renderer.draw_circle(
            Dimensions.get_circle_x_pt(), 
            Dimensions.get_circle_y_pt(), 
            Dimensions.get_circle_radius_pt(), 
            Colors.UCR_BLUE
        )
        
        # 4. Letra 'b'
        # Ajuste fino para centrar visualmente la 'b' (basado en pruebas visuales)
        # En cairo_test.py se usaba centrado automático, aquí usaremos "center"
        # pero el punto de anclaje es el centro del círculo.
        self.renderer.draw_text(
            "b", 
            Dimensions.get_circle_x_pt(), 
            Dimensions.get_circle_y_pt(), 
            Dimensions.get_font_size_b_pt(), 
            Colors.WHITE,
            align="center"
        )
        
        # 5. Nombre de la parada
        # Usar LayoutEngine para wrapping automático si es necesario
        layout = LayoutEngine(self.renderer.ctx, font_size=Dimensions.get_font_size_title_pt())
        max_width = Dimensions.get_default_width_pt() - Dimensions.get_text_margin_left_pt() - mm_to_pt(18)  # 18mm padding derecho
        
        lines = layout.wrap_text(stop_data.stop.name, max_width)
        
        # Si hay múltiples líneas, ajustar font_size si no cabe verticalmente
        text_height = layout.get_text_height(lines)
        available_height = Dimensions.get_default_height_pt() - Dimensions.get_circle_y_pt() - mm_to_pt(20)  # 20mm desde círculo
        
        if text_height > available_height and len(lines) > 1:
            # Reducir font_size proporcionalmente
            scale_factor = available_height / text_height
            new_font_size = Dimensions.get_font_size_title_pt() * scale_factor
            if new_font_size < mm_to_pt(8):  # 8mm mínimo
                new_font_size = mm_to_pt(8)
            layout = LayoutEngine(self.renderer.ctx, font_size=new_font_size)
            lines = layout.wrap_text(stop_name, max_width)
        
        # Posición Y: empezar desde abajo del círculo
        start_y = Dimensions.get_circle_y_pt() + Dimensions.get_circle_radius_pt() + mm_to_pt(10)  # 10mm abajo del círculo
        
        layout.draw_multiline_text(lines, Dimensions.get_text_margin_left_pt(), start_y, Colors.UCR_BLUE, align="left")
