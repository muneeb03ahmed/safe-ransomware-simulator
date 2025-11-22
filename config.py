from pydantic import BaseModel
from pathlib import Path
import json, sys

class LabConfig(BaseModel):
    lab_root: str
    sim_suffix: str = ".simlocked"
    ransom_note_name: str = "READ_ME_SIMULATED.txt"
    max_files: int = 200
    max_total_bytes: int = 50 * 1024 * 1024
    throttle_ms: int = 10
    telemetry_path: str | None = None

def load_config(path: Path | None = None) -> LabConfig:
    cand = path or Path.cwd() / ".labconfig.json"
    if not cand.exists():
        raise FileNotFoundError(f"Config not found: {cand}")
    data = json.loads(cand.read_text())
    cfg = LabConfig(**data)
    # safety: require marker file in lab_root
    lab_root = Path(cfg.lab_root).resolve()
    marker = lab_root / ".LAB_OK"
    if not marker.exists():
        raise RuntimeError(f"Lab root missing safety marker: {marker}")
    return cfg
