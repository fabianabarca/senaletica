from dataclasses import dataclass
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DOCS_DIR = BASE_DIR / "docs"
ASSETS_DIR = DOCS_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
SVG_DIR = ASSETS_DIR / "svg"

@dataclass
class Config:
    # Debug Toggle
    DEBUG_LAYOUT: bool = False
    
    # Identity Colors (CMYK approximates/Hex)
    UCR_BLUE: str = "#005DA4" # 100, 75, 0, 40 (CMYK approximation)
    UCR_CELESTE: str = "#00C0F3" # 100, 0, 0, 0
    WHITE: str = "#FFFFFF"
    BLACK: str = "#000000"
    
    # Fonts
    FONT_FAMILY: str = "Myriad Pro"
    # Note: Cairo/Linux needs the font installed or loaded.
    # We will try to load it via file path if possible or rely on system install.
    FONT_BOLD_PATH: str = str(FONTS_DIR / "MYRIADPRO-BOLD.OTF")
    
    # Assets
    LOGO_PATH: str = str(DOCS_DIR / "assets/logos/b_azul.png")

    # Dimensions (mm)
    # Vertical Sign
    VERTICAL_WIDTH: float = 450.0 
    VERTICAL_HEIGHT_MIN: float = 600.0 # Variable, but start here. 
    # The logo is 450mm diameter. 
    # Infrastructure md says: "Símbolo b tiene 45 cm de diámetro".
    # And text is below it.
    
    LOGO_DIAMETER: float = 450.0
    
    # Spacing
    LOGO_TEXT_GAP: float = 50.0 # "5 cm de separación vertical"

GLOBAL_CONFIG = Config()
