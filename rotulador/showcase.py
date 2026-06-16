import json
from pathlib import Path
from src.datalayer import DataLayer
from src.renderers.cairo import CairoRenderer
from src.templates.vertical import VerticalPostTemplate
from src.templates.experimental import HorizontalShelterTemplate, CircularVerticalTemplate

def main():
    # Setup
    renderer = CairoRenderer()
    output_dir = Path("output/showcase")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize Data Layer
    data_layer = DataLayer(Path("data"))
    
    try:
        # Load P005 (Microbiologia)
        stop = data_layer.load_stop("P005")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    print(f"Generating Showcase for: {stop.name} ({stop.id})")
    
    # 1. Standard Vertical
    print("1. Generando Layout Estandar (Vertical Original)...")
    tmpl_std = VerticalPostTemplate()
    spec_std = tmpl_std.generate_spec(stop.name)
    renderer.render(spec_std, str(output_dir / f"{stop.id}_standard.pdf"))
    
    # 2. Horizontal Shelter (Wide)
    print("2. Generando Layout Horizontal (Parada de Bus)...")
    tmpl_horz = HorizontalShelterTemplate()
    spec_horz = tmpl_horz.generate_spec(stop.name)
    renderer.render(spec_horz, str(output_dir / f"{stop.id}_horizontal.pdf"))
    
    # 3. Circular Logo Variation
    print("3. Generando Variacion de Logo (Circular)...")
    tmpl_circ = CircularVerticalTemplate()
    spec_circ = tmpl_circ.generate_spec(stop.name)
    renderer.render(spec_circ, str(output_dir / f"{stop.id}_circular.pdf"))

    print("\nShowcase Generation Complete! Check output/showcase/")

if __name__ == "__main__":
    main()
