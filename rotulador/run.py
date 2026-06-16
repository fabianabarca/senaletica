import argparse
from pathlib import Path
from src.core import Rotulo
from src.types import SignType
from src.datalayer import DataLayer

def main():
    parser = argparse.ArgumentParser(description="Generate bUCR signs")
    parser.add_argument("input_path", nargs='?', default="data/stops", help="Path to JSON file or directory (default: data/stops)")
    parser.add_argument("--output", "-o", help="Output directory or file (default: output/)")
    
    args = parser.parse_args()
    
    input_path = Path(args.input_path)
    # Initialize DataLayer
    data_layer = DataLayer(Path("data"))
    
    # Determine output directory
    if args.output:
        output_base = Path(args.output)
    else:
        output_base = Path("output")
        output_base.mkdir(parents=True, exist_ok=True)

    # Collect files to process
    files_to_process = []
    if input_path.is_file():
        files_to_process.append(input_path)
    elif input_path.is_dir():
        files_to_process.extend(input_path.glob("*.json"))
    else:
        print(f"Error: Input path '{input_path}' not found.")
        return

    if not files_to_process:
        print(f"No JSON files found in {input_path}")
        return

    print(f"Found {len(files_to_process)} stop definitions to process.")

    # Process each file
    rotulo = Rotulo()
    
    for json_file in files_to_process:
        try:
            process_file(rotulo, data_layer, json_file, output_base)
        except Exception as e:
            print(f"Failed to process {json_file}: {e}")

def process_file(rotulo, data_layer, json_file, output_base):
    # Load Data using DataLayer
    stop = data_layer.load_from_path(json_file)
    
    # Map Type
    if "vertical" in stop.sign_type:
        sign_type = SignType.VERTICAL
    else:
        sign_type = SignType.HORIZONTAL

    # Determine Output Path
    if output_base.suffix: # strictly if it looks like a file extension
         output_path = str(output_base)
    else:
         output_base.mkdir(exist_ok=True, parents=True)
         output_path = str(output_base / f"{stop.id}.pdf")

    # Generate
    print(f"Generating [{stop.id}] '{stop.name}'...")
    
    spec = rotulo.create_spec(sign_type, stop.name)
    rotulo.renderer.render(spec, output_path)

if __name__ == "__main__":
    main()
