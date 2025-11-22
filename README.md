# Ransomware-Lab-CLI

**Safe Ransomware Simulation CLI for Cyber Labs**

Ransomware-Lab-CLI is a safe, non-destructive command-line tool that simulates ransomware-like behaviour in a strictly controlled lab folder.  
It never encrypts data; instead it performs reversible file renames, creates a fake ransom note, records filesystem telemetry, detects suspicious patterns, and restores everything back.

---

## Features

- 🔐 **Safe simulation only**
  - No encryption, no persistence, no lateral movement.
  - Operates only inside an explicitly marked lab folder (`.LAB_OK`).

- 📁 **Lab initialization**
  - Sets up a sandbox directory with sample files and config.

- 👀 **Realtime monitoring**
  - Uses `watchdog` to log filesystem events to a JSONL telemetry file.

- 💣 **Ransomware-like activity**
  - Renames files by appending a `.simlocked` suffix.
  - Drops a clearly marked **simulated ransom note**.

- 🧠 **Heuristic detection**
  - Analyses telemetry for bursts of renames + ransom note presence.
  - Produces a simple verdict: `LOW` or `SUSPICIOUS`.

- 📊 **Auto-reporting**
  - Generates a Markdown report (`lab_run_report.md`) summarising the run.

- ♻️ **Full restore**
  - Reverts file names and removes the ransom note.
  - Designed to leave the lab in a clean state after each demo.

---

## Tech Stack

- **Language:** Python 3.11+
- **CLI:** [Typer](https://typer.tiangolo.com/)
- **Terminal UI:** [Rich](https://github.com/Textualize/rich)
- **Config & validation:** Pydantic
- **Filesystem monitoring:** Watchdog
- **Logging:** Loguru (optional if you add it)

---

## Installation

```bash
git clone https://github.com/<your-username>/ransomware-lab-cli.git
cd ransomware-lab-cli

# Create & activate virtualenv
python3.11 -m venv .venv
source .venv/bin/activate

# Install with dev extras
pip install -e ".[dev]"
