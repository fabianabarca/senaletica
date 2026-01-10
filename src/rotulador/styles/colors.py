"""
Definición de colores oficiales para bUCR.
Valores normalizados para Cairo (0.0 - 1.0).
Basado en: docs/elementos.md (Manual de Identidad Visual UCR 3.1)
"""

class Colors:
    # Azul UCR (#005DA4) - RGB: 0, 93, 164
    UCR_BLUE = (0.0, 0.365, 0.643)

    # Celeste UCR (#00C0F3) - RGB: 0, 192, 243
    UCR_CELESTE = (0.0, 0.753, 0.953)

    # Verde UCR (#6DC067) - RGB: 109, 192, 103
    UCR_GREEN = (0.427, 0.753, 0.404)

    # Amarillo UCR (#FFE06A) - RGB: 255, 224, 106
    UCR_YELLOW = (1.0, 0.878, 0.416)

    # Naranja UCR (#F37021) - RGB: 243, 112, 33
    UCR_ORANGE = (0.953, 0.439, 0.129)
    
    # Blanco (#FFFFFF)
    WHITE = (1.0, 1.0, 1.0)
    
    # Negro (#000000)
    BLACK = (0.0, 0.0, 0.0)
    
    # Gris (#CCCCCC) - Para guías o debug
    GRAY = (0.8, 0.8, 0.8)
