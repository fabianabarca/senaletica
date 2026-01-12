import cairo
import math
from typing import List, Tuple
from .base import Template
from ..types import SignSpec, SignType, OpLogo, OpText
from ..styles.config import GLOBAL_CONFIG
from ..layout.grid import LayoutGrid, Box

class VerticalPostTemplate(Template):
    def __init__(self):
        # Tools for measuring
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
        self.ctx = cairo.Context(self.surface)
        self.ctx.select_font_face(GLOBAL_CONFIG.FONT_FAMILY, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

    def generate_spec(self, stop_name: str) -> SignSpec:
        width_mm = GLOBAL_CONFIG.VERTICAL_WIDTH
        
        # Unified Content Margin (Global padding)
        global_margin = 25.0

        # Initialize Layout Grid
        grid = LayoutGrid(width_mm, 0)
        
        # --- STACK LAYOUT LOGIC ---
        cursor_y = global_margin
        
        # 1. Logo
        content_width = width_mm - (global_margin * 2)
        logo_size = content_width 
        
        logo_content_box = Box(
            x=global_margin,
            y=cursor_y,
            width=logo_size,
            height=logo_size,
            name="logo_content",
            color=(0.9, 0.6, 0) # Orange
        )
        grid.boxes.append(logo_content_box)
        cursor_y += logo_size
        
        # 2. Gap
        gap_h = GLOBAL_CONFIG.LOGO_TEXT_GAP # 50mm
        gap_box = Box(
            x=global_margin,
            y=cursor_y,
            width=content_width,
            height=gap_h,
            name="gap_separator",
            color=(0.6, 0.6, 0.6) # Gray
        )
        grid.boxes.append(gap_box) 
        cursor_y += gap_h
        
        # 3. Text Layout
        lines, font_size_pt = self._calculate_layout(stop_name, content_width)
        font_size_mm = font_size_pt / 2.83465
        line_height_total = len(lines) * font_size_mm * 1.1
        
        content_box = Box(
            x=global_margin,
            y=cursor_y,
            width=content_width,
            height=line_height_total,
            name="text_safe_area",
            color=(0, 0.5, 0) # Green 
        )
        grid.boxes.append(content_box)
        cursor_y += line_height_total

        # 4. Margin Bottom
        cursor_y += global_margin
        
        total_height = cursor_y
        
        # 5. Global Safe Zone (Red Box)
        safe_zone_box = Box(
            x=global_margin,
            y=global_margin,
            width=content_width,
            height=total_height - (global_margin * 2),
            name="safe_zone",
            color=(0.8, 0, 0) # Red
        )
        grid.boxes.append(safe_zone_box)

        # --- DYNAMIC OPS ASSIGNMENT (THE "LEGO" PART) ---
        dynamic_ops = []

        # A. Assign Logo to Top Box
        dynamic_ops.append(OpLogo(
            x=logo_content_box.x, 
            y=logo_content_box.y,
            width=logo_content_box.width, 
            height=logo_content_box.height
        ))

        # B. Assign Text to Bottom Box
        dynamic_ops.append(OpText(
            x=content_box.x, 
            y=content_box.y,
            width=content_box.width, 
            height=content_box.height,
            lines=lines, 
            font_size_pt=font_size_pt, 
            color_rgb=(0,0,0)
        ))

        # --- SCALABLE DEBUG GENERATION ---
        debug_boxes_flat = grid.flatten() if GLOBAL_CONFIG.DEBUG_LAYOUT else None

        return SignSpec(
            type=SignType.VERTICAL,
            stop_name=stop_name,
            width_mm=width_mm,
            height_mm=total_height,
            font_size_pt=font_size_pt,
            text_lines=lines,
            text_y_pos_mm=content_box.y,
            debug_boxes=debug_boxes_flat,
            render_ops=dynamic_ops
        )

    def _calculate_layout(self, text: str, max_width_mm: float) -> Tuple[List[str], float]:
        """
        Calculates the layout dynamically maximizing font size.
        Follows norms: Target ~300pt. Min Recommended ~200pt.
        """
        mm_to_pt = 2.83465
        max_width_pt = max_width_mm * mm_to_pt
        
        # 1. Measure text as single line at Reference Size (e.g. 100pt)
        ref_size = 100.0
        self.ctx.set_font_size(ref_size)
        extents = self.ctx.text_extents(text)
        w_ref = extents.width
        
        if w_ref == 0: return [text], 300 # Safety for empty string
        
        # 2. Calculate Max Possible Size (mathematically filling the width)
        # size / ref_size = max_width / w_ref
        max_possible_size = ref_size * (max_width_pt / w_ref)
        
        # 3. Apply Constraints (Target 300pt standard)
        # If it can be bigger than 300, cap it at 300 (or 350 max).
        chosen_size = min(max_possible_size, 320.0) 
        
        # 4. Check Minimal Standard (200pt)
        # Infrastructure doc says "Minimum 200pt".
        if chosen_size >= 200.0:
            # It fits comfortably or acceptably above standard.
            # Just to be safe with Cairo rendering quirks, lets take 95% of max possible to ensure margins
            final_size = min(chosen_size, max_possible_size * 0.95)
            return [text], final_size
            
        # 5. If we are here, Single Line < 200pt. 
        # We should try splitting into 2 lines to regain size.
        
        words = text.split()
        if len(words) == 1:
            # Single word case (e.g. "Microbiología")
            # We violate strict norm (<200pt) OR we hyphenate.
            # If size is "decent" (e.g. > 150), stick with it to avoid ugly hyphens.
            if chosen_size > 140.0:
                return [text], max_possible_size * 0.95
            
            # If it's REALLY small (e.g. < 140), force hyphenation.
            mid = len(text) // 2
            # Simple heuristic: Split at middle-ish vowel? 
            # Or just dumb split. "Micro-biología"
            part1 = text[:mid] + "-"
            part2 = text[mid:]
            lines = [part1, part2]
            
            # Recalculate size for 2 lines
            # Max width is same. We take the longest line.
            return self._calculate_multiline_size(lines, max_width_pt)
            
        else:
            # Multiple words (e.g. "Facultad de Ingeniería")
            # Find best split point
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
            lines = [line1, line2]
            return self._calculate_multiline_size(lines, max_width_pt)

    def _calculate_multiline_size(self, lines: List[str], max_width_pt: float) -> Tuple[List[str], float]:
        ref_size = 100.0
        self.ctx.set_font_size(ref_size)
        
        max_w_ref = 0
        for line in lines:
            max_w_ref = max(max_w_ref, self.ctx.text_extents(line).width)
            
        if max_w_ref == 0: return lines, 300
        
        max_possible_size = ref_size * (max_width_pt / max_w_ref)
        
        # Cap at 320pt standard
        final_size = min(max_possible_size * 0.95, 320.0)
        
        return lines, final_size

    def _fits(self, text: str, font_size: float, max_width: float) -> bool:
        self.ctx.set_font_size(font_size)
        extents = self.ctx.text_extents(text)
        return extents.width <= max_width

    def _fits_multiline(self, lines: List[str], font_size: float, max_width: float) -> bool:
        self.ctx.set_font_size(font_size)
        for line in lines:
            if self.ctx.text_extents(line).width > max_width:
                return False
        return True
