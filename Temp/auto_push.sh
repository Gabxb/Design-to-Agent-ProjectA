#!/bin/bash

# 自动 Git 推送脚本
# 功能：检测 /home/github 目录内文件改动，自动提交并推送

REPO_DIR="/home/github"
COMMIT_MSG="自动提交 - $(date '+%Y-%m-%d %H:%M:%S')"

echo "=== 自动 Git 推送脚本 ==="
echo "目标目录: $REPO_DIR"
echo ""

# 1. 检查目录是否存在
if [ ! -d "$REPO_DIR" ]; then
    echo "错误：目录 $REPO_DIR 不存在！"
    exit 1
fi

# 2. 进入目录
cd "$REPO_DIR" || exit 1

# 3. 检查是否是 Git 仓库
if [ ! -d ".git" ]; then
    echo "错误：当前目录不是 Git 仓库！"
    echo "请先执行：git init"
    exit 1
fi

# 4. 检测是否有改动（包括新增、修改、删除）
CHANGES=$(git status --porcelain)

if [ -z "$CHANGES" ]; then
    echo "检测结果：没有需要提交的文件。"
    echo "当前仓库已是最新状态。"
    exit 0
fi

echo "检测到以下改动："
echo "$CHANGES"
echo ""

# 5. 自动添加所有改动
echo "正在添加文件..."
git add .

# 6. 提交
echo "正在提交..."
git commit -m "$COMMIT_MSG"

# 7. 推送
echo "正在推送到远程仓库..."
if git push; then
    echo ""
    echo "✅ 推送成功！"
    echo "提交信息：$COMMIT_MSG"
else
    echo ""
    echo "❌ 推送失败！请检查网络或远程仓库状态。"
    exit 1
fi
