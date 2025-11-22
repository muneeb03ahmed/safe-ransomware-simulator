from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import json, time
from config import LabConfig

class _Handler(FileSystemEventHandler):
    def __init__(self, out):
        self.out = out
    def on_moved(self, event):
        if not event.is_directory:
            self._write("moved", src=event.src_path, dest=event.dest_path)
    def on_created(self, event):
        if not event.is_directory:
            self._write("created", path=event.src_path)
    def _write(self, kind, **data):
        data["kind"] = kind
        data["ts"] = time.time()
        self.out.write(json.dumps(data)+"\n"); self.out.flush()

def start_monitor(cfg: LabConfig):
    root = Path(cfg.lab_root)
    out_path = Path(cfg.telemetry_path or (root / "telemetry.jsonl"))
    with out_path.open("a", encoding="utf-8") as out:
        handler = _Handler(out)
        obs = Observer(); obs.schedule(handler, str(root), recursive=True)
        obs.start()
        print(f"Monitoring {root} -> {out_path}. Ctrl+C to stop.")
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            obs.stop(); obs.join()
