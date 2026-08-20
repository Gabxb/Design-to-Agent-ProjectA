# Render Mermaid tutorial sources to PNG and SVG wrappers.
# Usage: powershell -ExecutionPolicy Bypass -File scripts/generate_mindmaps.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python scripts/generate_mindmaps.py
