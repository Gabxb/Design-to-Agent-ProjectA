#!/usr/bin/env python3
"""Generate and validate the local AI Agent learning system."""

from __future__ import annotations

import argparse
from pathlib import Path

from roadmap_builder.generator import RoadmapGenerator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 AI Agent 本地学习系统")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--pdf-only", action="store_true", help="只重新生成 PDF")
    mode.add_argument("--check-only", action="store_true", help="只运行完整性检查")
    parser.add_argument("--skip-pdf", action="store_true", help="生成文本文件但跳过 PDF")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parent
    generator = RoadmapGenerator(root)

    if args.check_only:
        result = generator.validate(write_report=True)
    elif args.pdf_only:
        generator.generate_pdfs()
        result = generator.validate(write_report=True)
    else:
        generator.generate_text_files()
        if not args.skip_pdf:
            generator.generate_pdfs()
        result = generator.validate(write_report=True)
        generator.refresh_manifest()

    print(result.summary)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
