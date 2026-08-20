#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "progress"
target = ROOT / "backups" / datetime.now().strftime("%Y-%m-%d-%H%M%S") / "progress"
target.parent.mkdir(parents=True, exist_ok=True)
shutil.copytree(source, target)
print(target)
