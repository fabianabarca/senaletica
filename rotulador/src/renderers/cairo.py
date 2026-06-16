import cairo
import cairosvg
import io
import math
from typing import Tuple
from PIL import Image
from .base import Renderer
from ..types import SignSpec, SignType, OpLogo, OpText
from ..styles.config import GLOBAL_CONFIG

class CairoRenderer(Renderer):
    def __init__(self):
        self.mm_to_pt = 2.83465
        self.dpi = 300

    def render(self, spec: SignSpec, output_path: str):
        # Calculate Dimensions in Points
        width_pt = spec.width_mm * self.mm_to_pt
        height_pt = spec.height_mm * self.mm_to_pt
        
        # Create Surface
        if output_path.lower().endswith('.pdf'):
            surface = cairo.PDFSurface(output_path, width_pt, height_pt)
        else:
            surface = cairo.SVGSurface(output_path, width_pt, height_pt)
            
        ctx = cairo.Context(surface)
        
        # Scale to allow drawing in MM
        ctx.scale(self.mm_to_pt, self.mm_to_pt)
        
        # Draw Background (White)
        ctx.set_source_rgb(1, 1, 1)
        ctx.rectangle(0, 0, spec.width_mm, spec.height_mm)
        ctx.fill()
        
        # Draw Content
        # Evolution: If render_ops are present, they take precedence over legacy fields.
        if hasattr(spec, 'render_ops') and spec.render_ops:
            self._draw_ops(ctx, spec.render_ops)
        else:
            # Fallback to legacy fixed renderers
            self._draw_logo(ctx, spec)
            self._draw_text(ctx, spec)
        
        if spec.debug_boxes:
            self._draw_debug(ctx, spec)

        surface.finish()
        print(f"Rendered: {output_path}")

    def _draw_ops(self, ctx: cairo.Context, ops: list):
        """Executes the list of render operations."""
        for op in ops:
            if isinstance(op, OpLogo):
                self._render_op_logo(ctx, op)
            elif isinstance(op, OpText):
                self._render_op_text(ctx, op)

    def _render_op_logo(self, ctx: cairo.Context, op: OpLogo):
        # Generic Logo Renderer for any Rect
        logo_path = op.image_path if op.image_path else GLOBAL_CONFIG.LOGO_PATH
        try:
            img_surface = cairo.ImageSurface.create_from_png(logo_path)
            img_w = img_surface.get_width()
            img_h = img_surface.get_height()
            
            # Fit inside box (Maintain Aspect Ratio)
            scale_x = op.width / img_w
            scale_y = op.height / img_h
            scale = min(scale_x, scale_y)
            
            # Center in box
            final_w = img_w * scale
            final_h = img_h * scale
            
            off_x = op.x + (op.width - final_w) / 2
            off_y = op.y + (op.height - final_h) / 2
            
            ctx.save()
            ctx.translate(off_x, off_y)
            ctx.scale(scale, scale)
            ctx.set_source_surface(img_surface, 0, 0)
            ctx.paint()
            ctx.restore()
        except Exception as e:
            print(f"Error drawing logo op: {e}")
            
    def _render_op_text(self, ctx: cairo.Context, op: OpText):
        # Generic Text Renderer
        ctx.select_font_face("Myriad Pro", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_source_rgb(*op.color_rgb)
        
        font_size_mm = op.font_size_pt / self.mm_to_pt
        ctx.set_font_size(font_size_mm)
        
        # Simple Vertical Centering Calculation
        line_height = font_size_mm * 1.1
        total_text_h = len(op.lines) * line_height
        
        start_y = op.y + (op.height - total_text_h) / 2 + font_size_mm # Approx baseline
        
        y_cursor = start_y
        
        for line in op.lines:
            extents = ctx.text_extents(line)
            # Center X
            x = op.x + (op.width - extents.width) / 2
            
            ctx.move_to(x, y_cursor) 
            ctx.show_text(line)
            y_cursor += line_height

    def _draw_debug(self, ctx: cairo.Context, spec: SignSpec):
        """Draws debug bounding boxes."""
        ctx.save()
        ctx.set_line_width(2.0) # Thick lines (2mm)
        
        for box in spec.debug_boxes:
            color = getattr(box, 'color', (1, 0, 1))
            ctx.set_source_rgb(*color)
            ctx.rectangle(box.x, box.y, box.width, box.height)
            ctx.stroke()
        ctx.restore()

    def _draw_logo(self, ctx: cairo.Context, spec: SignSpec):
        # Logo Logic using PNG directly
        
        # If legacy positioning is missing, skip
        if spec.logo_size_mm is None or spec.logo_y_pos_mm is None:
            return

        # Use computed size if available, otherwise fallback to config
        w = spec.logo_size_mm
        
        # If size is effectively zero, do not draw (allows disabling legacy logo)
        if w <= 1.0:
            return

        h = w
        
        # Center horizontally based on the spec width
        x = (spec.width_mm - w) / 2
        
        y = spec.logo_y_pos_mm
        
        logo_path = GLOBAL_CONFIG.LOGO_PATH
        
        try:
            # Load ImageSurface from PNG directly
            # Cairo supports loading PNGs natively
            img_surface = cairo.ImageSurface.create_from_png(logo_path)
            
            # Calculate Scale
            img_w = img_surface.get_width()
            img_h = img_surface.get_height()
            
            # We want to draw this into rectangle (x, y, w, h)
            # Context is in MM scale (1 unit = 1 mm)
            
            ctx.save()
            ctx.translate(x, y)
            
            scale_x = w / img_w
            scale_y = h / img_h
            
            ctx.scale(scale_x, scale_y)
            
            ctx.set_source_surface(img_surface, 0, 0)
            ctx.paint()
            ctx.restore()
            
        except Exception as e:
            print(f"Error drawing logo: {e}")
            # Fallback
            ctx.set_source_rgb(0, 0.36, 0.64) 
            ctx.arc(x + w/2, y + h/2, w/2, 0, 2 * math.pi)
            ctx.fill()


    def _draw_text(self, ctx: cairo.Context, spec: SignSpec):
        # Text Logic
        # Font loading is still system dependent.
        # "Myriad Pro" or "MyriadPro-Bold"
        
        ctx.select_font_face("Myriad Pro", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        
        # Color Black
        ctx.set_source_rgb(0, 0, 0)
        
        y_cursor = spec.text_y_pos_mm
        
        # Line layout
        # We assume spec.text_lines contains the broken down lines
        font_size_mm = spec.font_size_pt / self.mm_to_pt
        
        ctx.set_font_size(spec.font_size_pt) # Font size is usually set in points, but here context is scaled to MM?
        # NO.
        # If context is scaled by `mm_to_pt`, then 1 unit = 1 point?
        # Verify:
        # ctx.scale(mm_to_pt, mm_to_pt) makes the coordinate space such that input 1 means 1mm.
        # But `set_font_size` usually expects User Space Units.
        # So providing `size_mm` would make sense?
        # If I want 300pt text. 300pt = 105.8mm.
        # If I call set_font_size(105.8), and CTM scales by 2.83.
        # Resulting size is 105.8 * 2.83 ~ 300 pixels/points on device. 
        # Correct. So I should pass MM to set_font_size if the CTM is in MM.
        
        # Wait, font_size_pt is given. Convert to MM.
        font_size_val = spec.font_size_pt / 2.83465  # Convert pt to mm
        ctx.set_font_size(font_size_val)
        
        line_height = font_size_val * 1.0 # Tight spacing mentioned in docs
        
        for line in spec.text_lines:
            extents = ctx.text_extents(line)
            # Center X
            x = (spec.width_mm - extents.width) / 2
            
            ctx.move_to(x, y_cursor + extents.height) # Move to baseline-ish
            ctx.show_text(line)
            
            y_cursor += line_height
