import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = BASE_DIR / "docs"
ASSETS_DIR = DOCS_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
SVG_DIR = ASSETS_DIR / "svg"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

# Identity Colors (from elements.md)
class Color:
    CELESTE_UCR = "#00C0F3"
    AZUL_UCR = "#005DA4"
    WHITE = "#FFFFFF"
    BLACK = "#000000"

# Sign Configuration (Dimensions in mm)
POST_WIDTH_MM = 300
POST_HEIGHT_MM = 600  # Approximation for now
