"""
Manejo de carga de fuentes.
"""
import cairo
import os
import warnings

class FontLoader:
    """
    Encargado de cargar y configurar fuentes para Cairo.
    """
    
    DEFAULT_FONT = "Myriad Pro"
    FALLBACK_FONT = "Sans"
    
    @staticmethod
    def load_font(ctx: cairo.Context, font_family: str = DEFAULT_FONT, 
                  weight: cairo.FontWeight = cairo.FONT_WEIGHT_BOLD,
                  slant: cairo.FontSlant = cairo.FONT_SLANT_NORMAL):
        """
        Configura la fuente en el contexto de Cairo.
        Intenta usar la fuente solicitada, si no está disponible, usa fallback.
        """
        # Nota: pycairo usa fontconfig/sistema para resolver nombres de fuentes.
        # No podemos cargar un archivo .otf directamente sin usar freetype-py.
        # Por ahora, confiamos en que la fuente esté instalada en el sistema.
        
        try:
            ctx.select_font_face(font_family, slant, weight)
            # TODO: Verificar si realmente se cargó la fuente correcta o un fallback
            # Cairo no lanza excepción si no encuentra la fuente, usa un default.
        except Exception as e:
            warnings.warn(f"Error cargando fuente {font_family}: {e}")
            ctx.select_font_face(FontLoader.FALLBACK_FONT, slant, weight)

    @staticmethod
    def get_font_path(font_filename: str) -> str:
        """
        Devuelve la ruta absoluta a un archivo de fuente en assets.
        Útil para embedding o scripts externos.
        """
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, "assets", "fonts", font_filename)
