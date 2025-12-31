#!/usr/bin/env python3
"""
Script de demostración del MVP de rotulador.
"""
import sys
import os

# Agregar src al path para poder importar rotulador sin instalarlo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import rotulador

def main():
    print("Iniciando demo de rotulador MVP...")
    
    try:
        # 1. Crear rótulo de prueba
        print("Generando rótulo para 'Facultad de Ingeniería'...")
        sign = rotulador.create("stop_back", stop_name="Facultad de Ingeniería")
        
        # 2. Exportar a SVG
        output_file = "demo_fing.svg"
        sign.export(output_file)
        print(f"✓ Exportado a {output_file}")
        
        # 3. Exportar a PNG (si cairo tiene soporte PNG, que usualmente sí)
        output_png = "demo_fing.png"
        sign.export(output_png)
        print(f"✓ Exportado a {output_png}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
