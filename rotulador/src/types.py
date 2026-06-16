from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Union, Tuple

class SignType(Enum):
    """Types of signs available in the system."""
    VERTICAL = "vertical"       # Standard vertical post (Logo + Name)
    HORIZONTAL = "horizontal"   # Horizontal shelter sign

class SignFormat(Enum):
    PDF = "pdf"
    SVG = "svg"

# -- Dynamic Content Operations --
@dataclass
class RenderOp:
    """Base class for rendering operations."""
    pass

@dataclass
class OpLogo(RenderOp):
    """Render the standard logo within a bounding box."""
    x: float
    y: float
    width: float
    height: float
    image_path: Optional[str] = None # Path to specific image asset

@dataclass
class OpText(RenderOp):
    """Render text lines within a bounding box."""
    x: float
    y: float
    width: float
    height: float
    lines: List[str]
    font_size_pt: float
    color_rgb: Tuple[float, float, float] = (0, 0, 0)
    align: str = "center" # center, left, right

@dataclass
class SignSpec:
    """Complete specification to render a sign."""
    type: SignType
    stop_name: str
    
    # Dimensions in mm
    width_mm: float
    height_mm: float
    
    # Text Layout (Legacy/Main fields)
    font_size_pt: float
    text_lines: List[str]
    
    # Positioning (computed by template)
    logo_y_pos_mm: Optional[float] = None
    logo_size_mm: Optional[float] = None
    text_y_pos_mm: Optional[float] = None

    # Dynamic Rendering Operations (The text/logo sub-elements)
    render_ops: List[RenderOp] = field(default_factory=list)

    # Debug info
    debug_boxes: Optional[List] = field(default=None) # List[Box] from layout.grid
    
    def __post_init__(self):
        if self.width_mm <= 0 or self.height_mm <= 0:
            raise ValueError("Dimensions must be positive")

