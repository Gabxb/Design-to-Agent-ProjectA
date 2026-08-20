# 自动化脚本

运行环境：Python 3.12。首次使用先在项目根目录执行 `python -m pip install -r requirements.txt`。

- `setup.sh` / `setup.ps1`：创建虚拟环境、安装依赖、生成文件与 PDF。
- `generate_pdfs.sh` / `generate_pdfs.ps1`：只从 Markdown 重新生成 PDF。
- `check_files.py`：检查目录、数量、JSON/YAML、Python、链接、密钥模式和 PDF。
- `backup_progress.py`：单独备份 `progress/`。

macOS/Linux 使用 Shell 脚本；Windows PowerShell 使用 `.ps1` 脚本。中文 PDF 需要系统中有 Noto Sans CJK、苹方、微软雅黑、黑体或其他可嵌入中文字体；也可通过 `ROADMAP_CJK_FONT` 指定字体文件。
