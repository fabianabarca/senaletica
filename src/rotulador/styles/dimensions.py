"""
Dimensiones estándar para rótulos bUCR.
Todas las medidas en milímetros (mm). Se convierten a puntos (pt) en tiempo de renderizado.
Basado en medidas físicas reales para impresión profesional.
"""

from ..utils.conversion import mm_to_pt

class Dimensions:
    # Canvas por defecto (ejemplo: tamaño típico de rótulo vertical)
    DEFAULT_WIDTH_MM = 450  # mm
    DEFAULT_HEIGHT_MM = 300  # mm
    
    # Elementos del rótulo Stop Back
    CIRCLE_RADIUS_MM = 28  # mm (aprox. 80 pt)
    CIRCLE_X_MM = 53  # mm
    CIRCLE_Y_MM = 53  # mm
    
    # Tamaños de fuente en mm (altura aproximada)
    FONT_SIZE_B_MM = 42  # mm (aprox. 120 pt)
    FONT_SIZE_TITLE_MM = 17  # mm (aprox. 48 pt)
    
    # Márgenes en mm
    TEXT_MARGIN_LEFT_MM = 88  # mm
    
    @classmethod
    def get_default_width_pt(cls) -> float:
        return mm_to_pt(cls.DEFAULT_WIDTH_MM)
    
    @classmethod
    def get_default_height_pt(cls) -> float:
        return mm_to_pt(cls.DEFAULT_HEIGHT_MM)
    
    @classmethod
    def get_circle_radius_pt(cls) -> float:
        return mm_to_pt(cls.CIRCLE_RADIUS_MM)
    
    @classmethod
    def get_circle_x_pt(cls) -> float:
        return mm_to_pt(cls.CIRCLE_X_MM)
    
    @classmethod
    def get_circle_y_pt(cls) -> float:
        return mm_to_pt(cls.CIRCLE_Y_MM)
    
    @classmethod
    def get_font_size_b_pt(cls) -> float:
        return mm_to_pt(cls.FONT_SIZE_B_MM)
    
    @classmethod
    def get_font_size_title_pt(cls) -> float:
        return mm_to_pt(cls.FONT_SIZE_TITLE_MM)
    
    @classmethod
    def get_text_margin_left_pt(cls) -> float:
        return mm_to_pt(cls.TEXT_MARGIN_LEFT_MM)
