from .base import SignTemplate
from ..styles.colors import Colors
from ..styles.dimensions import Dimensions

class StopBackTemplate(SignTemplate):
    """
    Plantilla para rótulo de respaldo (Stop Back).
    Diseño: Círculo azul con 'b' blanca + Nombre de parada.
    """
    
    def render(self, stop_name: str):
        # 1. Setup canvas
        self.renderer.setup(Dimensions.DEFAULT_WIDTH, Dimensions.DEFAULT_HEIGHT)
        
        # 2. Background (Blanco)
        self.renderer.draw_background(Colors.WHITE)
        
        # 3. Círculo Azul
        self.renderer.draw_circle(
            Dimensions.CIRCLE_X, 
            Dimensions.CIRCLE_Y, 
            Dimensions.CIRCLE_RADIUS, 
            Colors.UCR_BLUE
        )
        
        # 4. Letra 'b'
        # Ajuste fino para centrar visualmente la 'b' (basado en pruebas visuales)
        # En cairo_test.py se usaba centrado automático, aquí usaremos "center"
        # pero el punto de anclaje es el centro del círculo.
        self.renderer.draw_text(
            "b", 
            Dimensions.CIRCLE_X, 
            Dimensions.CIRCLE_Y, 
            Dimensions.FONT_SIZE_B, 
            Colors.WHITE,
            align="center"
        )
        
        # 5. Nombre de la parada
        # Ajuste automático de tamaño si el texto es muy largo
        font_size = Dimensions.FONT_SIZE_TITLE
        max_width = Dimensions.DEFAULT_WIDTH - Dimensions.TEXT_MARGIN_LEFT - 50 # 50px padding derecho
        
        text_width = self.renderer.get_text_width(stop_name, "Myriad Pro", font_size)
        
        if text_width > max_width:
            # Reducir tamaño proporcionalmente
            scale_factor = max_width / text_width
            font_size = font_size * scale_factor
            # Limite inferior para legibilidad
            if font_size < 24:
                font_size = 24
                # Aquí idealmente haríamos word-wrap, pero para MVP reducimos tamaño
        
        # Calcular posición Y para centrar verticalmente respecto al círculo
        # O usar una posición fija como en el diseño original
        text_y = Dimensions.CIRCLE_Y + (font_size / 3) # Ajuste visual de baseline
        
        self.renderer.draw_text(
            stop_name,
            Dimensions.TEXT_MARGIN_LEFT,
            text_y,
            font_size,
            Colors.UCR_BLUE,
            align="left" # Alineado a la izquierda del margen
        )
