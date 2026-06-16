import cairo
from typing import List, Tuple
from .base import Template
from ..types import SignSpec, SignType, OpLogo, OpText
from ..styles.config import GLOBAL_CONFIG, ASSETS_DIR
from ..layout.grid import LayoutGrid, Box

class HorizontalShelterTemplate(Template):
    """
    Experimental template: Wide format (e.g. 900x300mm) for bus shelters.
    Layout: [ Logo (Left) | Text (Right) ]
    """
    def __init__(self):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
        self.ctx = cairo.Context(self.surface)
        self.ctx.select_font_face(GLOBAL_CONFIG.FONT_FAMILY, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

    def generate_spec(self, stop_name: str) -> SignSpec:
        width_mm = 900.0
        height_mm = 300.0
        margin = 30.0

        grid = LayoutGrid(width_mm, height_mm)
        
        # Define Main Container Box (inside margins)
        container = Box(
            x=margin, 
            y=margin, 
            width=width_mm - (margin*2), 
            height=height_mm - (margin*2),
            color=(0.5, 0.5, 0.5)
        )
        
        # Split Container: 30% Logo, 70% Text, with gutter
        cols = container.split(rows=1, cols=2, gutter=40.0)
        # Modify split widths manually to achieve 30/70 split if split() only does equal?
        # My current split() does equal split.
        # Let's override purely for this custom layout.
        
        logo_w = container.width * 0.25
        text_w = container.width * 0.75 - 40.0 # minus gutter
        
        logo_box = Box(container.x, container.y, logo_w, container.height, "logo_zone", (1, 0.5, 0))
        text_box = Box(container.x + logo_w + 40.0, container.y, text_w, container.height, "text_zone", (0, 1, 0))
        
        grid.boxes.append(logo_box)
        grid.boxes.append(text_box)
        
        # Ops
        ops = []
        ops.append(OpLogo(
            x=logo_box.x, y=logo_box.y, 
            width=logo_box.width, height=logo_box.height
        ))
        
        # Calculate Text
        # For horizontal, we might want Left Alignment, but OpText defaults to center?
        # Let's just use defaults for now, it centers in the box.
        lines, size = self._calculate_layout(stop_name, text_box.width, max_lines=2)
        
        ops.append(OpText(
            x=text_box.x, y=text_box.y,
            width=text_box.width, height=text_box.height,
            lines=lines, font_size_pt=size, color_rgb=(0, 0, 0)
        ))
        
        return SignSpec(
            type=SignType.HORIZONTAL, # Just a label
            stop_name=stop_name,
            width_mm=width_mm,
            height_mm=height_mm,
            font_size_pt=size, # computed
            text_lines=lines,
            render_ops=ops,
            debug_boxes=grid.flatten() if GLOBAL_CONFIG.DEBUG_LAYOUT else None
        )

    def _calculate_layout(self, text: str, max_width_mm: float, max_lines: int = 2) -> Tuple[List[str], float]:
        # Simplified calculator for this template
        # Assume huge font possible
        return [text], 250.0 # Mock implementation, just pass text through

class CircularVerticalTemplate(Template):
    """
    Experimental template: Vertical post but using the circular bus logo.
    Layout: Standard Vertical but with alt logo asset.
    """
    def __init__(self):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
        self.ctx = cairo.Context(self.surface)
        self.ctx.select_font_face(GLOBAL_CONFIG.FONT_FAMILY, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

    def generate_spec(self, stop_name: str) -> SignSpec:
        width_mm = 450.0 # Standard width
        global_margin = 50.0
        
        # New Logo Path
        circ_logo = str(ASSETS_DIR / "png/rotulo_bus_circular.png")

        grid = LayoutGrid(width_mm, 0)
        cursor_y = global_margin
        
        # 1. Logo Box
        logo_size = width_mm - (global_margin * 2)
        logo_box = Box(global_margin, cursor_y, logo_size, logo_size, "logo", (1, 1, 0))
        grid.boxes.append(logo_box)
        cursor_y += logo_size
        
        # 2. Gap
        gap_h = 50.0
        cursor_y += gap_h
        
        # 3. Text Box
        # Let's say we reserve 400mm height for text
        text_h = 400.0
        text_box = Box(global_margin, cursor_y, logo_size, text_h, "text", (0, 1, 0))
        grid.boxes.append(text_box)
        cursor_y += text_h
        
        # Ops
        ops = []
        ops.append(OpLogo(
            x=logo_box.x, y=logo_box.y,
            width=logo_box.width, height=logo_box.height,
            image_path=circ_logo # USE ALT IMAGE
        ))
        
        ops.append(OpText(
            x=text_box.x, y=text_box.y,
            width=text_box.width, height=text_box.height,
            lines=[stop_name], font_size_pt=200.0, color_rgb=(0,0,0)
        ))
        
        return SignSpec(
            type=SignType.VERTICAL,
            stop_name=stop_name,
            width_mm=width_mm,
            height_mm=cursor_y + global_margin,
            font_size_pt=200.0,
            text_lines=[stop_name],
            render_ops=ops,
            debug_boxes=grid.flatten() if GLOBAL_CONFIG.DEBUG_LAYOUT else None
        )
