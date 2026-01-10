import sys
import os

# Agregar src al path para poder importar rotulador sin instalarlo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import rotulador
from rotulador.utils.parser import RoutesParser
from rotulador.models import Stop

def main():
    print("Iniciando demo de rotulador MVP...")
    
    try:
        # 1. Parsear datos de rutas
        parser = RoutesParser.from_file("research/05-scalability/routes.md")
        data = parser.parse()
        print(f"✓ Parseadas {len(data['routes'])} rutas y {len(data['schedules'])} horarios")
        
        # 2. Crear StopData para demo
        stop = Stop(
            id="facultad_ingenieria",
            name="Facultad de Ingeniería",
            latitude=9.937,  # Coordenadas aproximadas UCR
            longitude=-84.052
        )
        
        from rotulador.models import StopData
        stop_data = StopData(
            stop=stop,
            routes=data['routes'],
            schedules=data['schedules'][:5]  # Primeros 5 horarios
        )
        
        # 3. Generar rótulo
        print("Generando rótulo para 'Facultad de Ingeniería'...")
        sign = rotulador.create("stop_back", stop_data=stop_data)
        
        # 4. Exportar a SVG
        output_file = "demo_fing.svg"
        sign.export(output_file)
        print(f"✓ Exportado a {output_file}")
        
        # 5. Exportar a PNG
        output_png = "demo_fing.png"
        sign.export(output_png)
        print(f"✓ Exportado a {output_png}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
