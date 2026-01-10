"""
Utilidades de conversión para el sistema de rotulación.
"""

def mm_to_pt(mm: float) -> float:
    """
    Convierte milímetros a puntos (pt).
    Cairo usa puntos como unidad base.
    1 mm ≈ 2.83465 pt
    """
    return mm * 2.834645669

def pt_to_mm(pt: float) -> float:
    """
    Convierte puntos a milímetros.
    """
    return pt / 2.834645669