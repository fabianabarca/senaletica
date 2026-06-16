import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any

@dataclass
class StopData:
    id: str
    name: str
    sign_type: str = "vertical"

class DataLayer:
    """
    Handles data ingestion and normalization.
    Acts as the single source of truth for loading stop information,
    masking the differences between legacy (Spanish) and new (English) data formats.
    """
    def __init__(self, data_root: Path):
        self.stops_dir = data_root / "stops"

    def load_stop(self, stop_id: str) -> StopData:
        # Construct path, handle extension if missing
        if not stop_id.endswith(".json"):
            filename = f"{stop_id}.json"
        else:
            filename = stop_id
            
        path = self.stops_dir / filename
        
        if not path.exists():
            raise FileNotFoundError(f"Stop file not found: {path}")
            
        return self._parse_file(path)

    def load_from_path(self, path: Path) -> StopData:
        """Load and normalize stop data directly from a specific file path."""
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return self._parse_file(path)

    def _parse_file(self, path: Path) -> StopData:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
            
        # Normalize keys (handle legacy Spanish vs new English)
        stop_id = raw.get("id") or raw.get("codigo") or "UNKNOWN"
        name = raw.get("name") or raw.get("nombre") or "Unknown Stop"
        sign_type = raw.get("sign_type") or raw.get("tipo") or "vertical"
        
        return StopData(id=stop_id, name=name, sign_type=sign_type)
