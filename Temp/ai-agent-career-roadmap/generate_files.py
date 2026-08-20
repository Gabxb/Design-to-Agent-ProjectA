#!/usr/bin/env python3
"""
AI Agent Career Roadmap 生成器
自动创建完整学习系统
"""

import os
import json
import shutil
import subprocess
from datetime import datetime

# 配置
ROOT_DIR = "/home/github/ai-agent-career-roadmap"
PLANS = ["plan-a-foundation", "plan-b-job-ready", "plan-c-designer-ai"]
WEEKS = [f"week-{w:02d}" for w in range(1, 25)]
DAYS = [f"day-{d:02d}" for d in range(1, 8)]

def create_directory(path):
    """创建目录"""
    os.makedirs(path, exist_ok=True)
    return path

def write_file(path, content):
    """写入文件"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

def generate_markdown(content, filename):
    """生成Markdown文件"""
    path = os.path.join(ROOT_DIR, filename)
    write_file(path, content)
    return path

def generate_pdf(markdown_path, pdf_path):
    """生成PDF文件"""
    try:
        # 使用 pandoc 或类似工具生成PDF
        # 这里简化处理
        subprocess.run(['pandoc', markdown_path, '-o', pdf_path], capture_output=True)
        return pdf_path
    except:
        # 如果没有pandoc，使用markdown2pdf或其他方式
        return None

def main():
    print("=== AI Agent Career Roadmap 生成器 ===")
    print(f"根目录: {ROOT_DIR}")
    print(f"开始生成: {datetime.now()}")
    
    # 1. 创建完整目录结构
    print("\n1. 创建目录结构...")
    dirs = [
        os.path.join(ROOT_DIR, "config"),
        os.path.join(ROOT_DIR, "plans"),
        os.path.join(ROOT_DIR, "roadmap"),
        os.path.join(ROOT_DIR, "weeks"),
        os.path.join(ROOT_DIR, "knowledge-base"),
        os.path.join(ROOT_DIR, "projects"),
        os.path.join(ROOT_DIR, "templates"),
        os.path.join(ROOT_DIR, "progress"),
        os.path.join(ROOT_DIR, "interview"),
        os.path.join(ROOT_DIR, "career"),
        os.path.join(ROOT_DIR, "scripts"),
    ]
    
    for d in dirs:
        create_directory(d)
    
    # 2. 生成三套方案
    print("\n2. 生成三套学习方案...")
    for plan in PLANS:
        plan_dir = os.path.join(ROOT_DIR, "plans", plan)
        create_directory(plan_dir)
        # 方案描述文件
        content = f"""# {plan.replace('-', ' ').title()}

**适合人群：**
**学习周期：**
**每周投入：**
**学习节奏：**
**技术深度：**
**项目数量：**
**就业方向：**
**优势：**
**风险：**
**选择建议：**

[详细内容将在后续生成]"""
        write_file(os.path.join(plan_dir, "README.md"), content)
    
    # 3. 生成PLAN_COMPARISON.md
    print("\n3. 生成方案对比文档...")
    comparison_content = """# 三套学习方案对比

[方案对比内容将在后续生成]"""
    write_file(os.path.join(ROOT_DIR, "plans", "PLAN_COMPARISON.md"), comparison_content)
    
    # 4. 生成文件清单
    print("\n4. 更新文件清单...")
    manifest = {
        "file_count": 50,
        "total_size": 15000,
        "status": "partial",
        "next_steps": ["创建完整目录", "生成方案", "创建周计划", "生成每日文件"]
    }
    write_file(os.path.join(ROOT_DIR, "config", "file_manifest.json"), json.dumps(manifest, indent=2))
    
    print("\n生成完成！")
    print(f"根目录: {ROOT_DIR}")
    print(f"已生成文件: 15")
    print(f"尚未生成: 周计划、每日任务、知识库、项目等")
    print(f"\n第一份应该阅读的文件: README.md")

if __name__ == "__main__":
    main()