import argparse
import sys
from . import create

def main():
    parser = argparse.ArgumentParser(description="Generador de rótulos bUCR")
    parser.add_argument("type", help="Tipo de rótulo (ej: stop_back)")
    parser.add_argument("text", help="Texto del rótulo (ej: Nombre de parada)")
    parser.add_argument("--output", "-o", default="output.svg", help="Archivo de salida")
    
    args = parser.parse_args()
    
    try:
        print(f"Generando rótulo '{args.type}' con texto: '{args.text}'...")
        sign = create(args.type, stop_name=args.text)
        sign.export(args.output)
        print(f"✓ Rótulo guardado en: {args.output}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
