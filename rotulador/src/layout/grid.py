from dataclasses import dataclass, field
from typing import List, Optional, Tuple

@dataclass
class Box:
    """Represents a rectangular region on the canvas."""
    x: float
    y: float
    width: float
    height: float
    name: str = "box"
    color: tuple = (1, 0, 1) # Magenta default for debug
    children: List['Box'] = field(default_factory=list)

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height
    
    @property
    def center_x(self) -> float:
        return self.x + (self.width / 2)
        
    @property
    def center_y(self) -> float:
        return self.y + (self.height / 2)

    def add_child(self, x: float, y: float, w: float, h: float, name: str, color: tuple = (0, 1, 1)) -> 'Box':
        """Adds a child box relative to this box's position (if x/y are relative, or absolute?). 
        For simplicity in this project, inputs are ABSOLUTE coordinates.
        """
        child = Box(x, y, w, h, name, color)
        self.children.append(child)
        return child
        
    def split(self, rows: int, cols: int, gutter: float = 0) -> List['Box']:
        """Splits the box into a grid of sub-boxes and adds them as children.
        Returns the list of created children.
        """
        cell_w = (self.width - (gutter * (cols - 1))) / cols
        cell_h = (self.height - (gutter * (rows - 1))) / rows
        
        new_boxes = []
        for r in range(rows):
            for c in range(cols):
                bx = self.x + (c * (cell_w + gutter))
                by = self.y + (r * (cell_h + gutter))
                child = Box(bx, by, cell_w, cell_h, f"{self.name}_r{r}_c{c}", self.color)
                self.children.append(child)
                new_boxes.append(child)
        return new_boxes

    def get_all_boxes(self) -> List['Box']:
        """Returns a flat list of self and all descendants."""
        all_b = [self]
        for c in self.children:
            all_b.extend(c.get_all_boxes())
        return all_b

@dataclass
class LayoutGrid:
    """Manages the defining boxes of a layout."""
    width: float
    height: float # Can be dynamic for vertical signs
    boxes: List[Box] = field(default_factory=list)
    
    def add_box(self, x: float, y: float, w: float, h: float, name: str, color: tuple = (1, 0, 1)) -> Box:
        box = Box(x, y, w, h, name, color)
        self.boxes.append(box)
        return box
    
    def flatten(self) -> List[Box]:
        """Returns flat list of all boxes in the grid for rendering."""
        flat = []
        for b in self.boxes:
            flat.extend(b.get_all_boxes())
        return flat

