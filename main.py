import typer
from pathlib import Path
from rich.console import Console
from config import LabConfig, load_config
from simulator import run_simulation
from monitor import start_monitor
from detector import run_detection
from restore import snapshot_lab, restore_lab
from report import generate_report
import json

app = typer.Typer()
console = Console()

@app.command()
def init(lab_root: Path = typer.Option(..., help="Path to lab root (must be empty or dedicated)")):
    lab_root.mkdir(parents=True, exist_ok=True)
    (lab_root / ".LAB_OK").write_text("AUTHORIZED LAB FOLDER\n")
    (lab_root / "docs").mkdir(exist_ok=True)
    (lab_root / "docs" / "invoice1.txt").write_text("Sample invoice content\n")
    cfg = LabConfig(lab_root=str(lab_root))
    Path(lab_root / ".labconfig.json").write_text(cfg.model_dump_json(indent=2))
    console.print(f"[green]Lab initialized at[/] {lab_root}")

@app.command()
def simulate(config: Path = typer.Option(None), dry_run: bool = False):
    cfg = load_config(config)
    snapshot_lab(cfg)
    run_simulation(cfg, dry_run=dry_run)

@app.command()
def monitor(config: Path = typer.Option(None)):
    cfg = load_config(config)
    start_monitor(cfg)

@app.command()
def detect(config: Path = typer.Option(None), telemetry: Path = typer.Option(None)):
    cfg = load_config(config)
    run_detection(cfg, telemetry)

@app.command()
def restore(config: Path = typer.Option(None)):
    cfg = load_config(config)
    restore_lab(cfg)

@app.command()
def report(config: Path = typer.Option(None), output: Path = Path("lab_run_report.md")):
    cfg = load_config(config)
    generate_report(cfg, output)
    console.print(f"Report written to {output}")

if __name__ == "__main__":
    app()
