import json
from pathlib import Path
from config import LabConfig

def run_detection(cfg: LabConfig, telemetry: Path | None):
    root = Path(cfg.lab_root)
    telem = Path(telemetry or (root / "telemetry.jsonl"))
    if not telem.exists():
        print("No telemetry.")
        return
    moves = []
    with telem.open() as f:
        for ln in f:
            try:
                ev = json.loads(ln)
                if ev.get("kind") == "moved":
                    moves.append(ev)
            except:
                pass
    suffix_moves = [m for m in moves if str(m.get("dest","")).endswith(cfg.sim_suffix)]
    score = 0
    if len(moves) >= 30: score += 2
    if len(suffix_moves) >= 20: score += 3
    if (root / cfg.ransom_note_name).exists(): score += 2
    verdict = "SUSPICIOUS" if score >= 4 else "LOW"
    print(f"Detection verdict: {verdict} (score={score})")
