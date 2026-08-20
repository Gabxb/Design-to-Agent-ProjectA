#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from roadmap_builder.generator import RoadmapGenerator

result = RoadmapGenerator(ROOT).validate(write_report=True)
print(result.summary)
raise SystemExit(0 if result.ok else 1)
