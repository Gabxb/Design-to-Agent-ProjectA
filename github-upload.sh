#!/bin/bash
# 一键上传到 GitHub 脚本
# 用法: ./github-upload.sh [仓库名] [本地目录]

set -e

echo "=== 一键上传到 GitHub ==="

# 安装 GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "正在安装 GitHub CLI..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y gh
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y gh
    elif command -v yum &> /dev/null; then
        sudo yum install -y gh
    else
        echo "❌ 请手动安装 GitHub CLI: https://cli.github.com/"
        exit 1
    fi
    echo "✅ GitHub CLI 安装完成"
fi

# 创建上传工具
UPLOAD_DIR="$HOME/.local/bin"
mkdir -p "$UPLOAD_DIR"

cat > "$UPLOAD_DIR/github-upload" << 'UPLOADER'
#!/bin/bash
# GitHub 一键上传工具 - 支持 SSH Key 认证
# 用法: github-upload [仓库名] [本地目录]

REPO_NAME=""
LOCAL_DIR="."

if [ $# -eq 1 ]; then
    REPO_NAME="$1"
elif [ $# -eq 2 ]; then
    REPO_NAME="$1"
    LOCAL_DIR="$2"
elif [ $# -gt 2 ]; then
    echo "用法: github-upload [仓库名] [本地目录]"
    exit 1
fi

if [ -z "$REPO_NAME" ]; then
    echo "请输入仓库名 (例如: username/repo) 或直接按 Enter 使用当前目录:"
    read -p "仓库名: " REPO_NAME
fi

# 登录 GitHub (支持 SSH Key 方式)
echo "正在处理 GitHub 登录 (支持 SSH Key 认证)..."
if ! gh auth status &> /dev/null; then
    echo "需要 GitHub 登录..."
    echo "使用 SSH Key 方式:"
    echo "1. 在 GitHub 官网 -> 设置 -> SSH 和 GPG keys -> 管理 SSH keys -> 添加新密钥"
    echo "2. 复制你的 SSH 公钥 (ssh-rsa 或 ecdsa) 到 GitHub"
    echo "3. 确保 SSH 密钥已添加"
    gh auth login --web
fi

# 进入指定目录
if [ "$LOCAL_DIR" != "." ]; then
    if [ ! -d "$LOCAL_DIR" ]; then
        echo "❌ 目录不存在: $LOCAL_DIR"
        exit 1
    fi
    cd "$LOCAL_DIR"
fi

# 获取仓库名称
REPO_NAME=${REPO_NAME:-$(basename "$(pwd)")}

echo "正在处理仓库: $REPO_NAME"

# 初始化 Git
if [ ! -d .git ]; then
    echo "初始化 Git 仓库..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# 检查远端
if ! git remote get-url origin &> /dev/null; then
    echo "创建 GitHub 仓库: $REPO_NAME"
    gh repo create "$REPO_NAME" --public --source=. --remote --push
    echo "✅ 仓库创建并上传完成"
else
    echo "仓库已存在，正在推送到 GitHub..."
    git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null || git push -u origin HEAD
    echo "✅ 推送完成"
fi

echo "🎉 上传成功！"
echo "访问地址: https://github.com/$(gh repo view --json owner -q '.owner.login')/$(gh repo view --json name -q '.name')"
UPLOADER

chmod +x "$UPLOAD_DIR/github-upload"

# 添加到 PATH
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$rc" ] && ! grep -q "$UPLOAD_DIR" "$rc" 2>/dev/null; then
        echo "export PATH=\$PATH:$UPLOAD_DIR" >> "$rc"
    fi
done

echo "✅ 安装完成！"
echo "使用方法："
echo "  cd /path/to/your/project"
echo "  github-upload username/repo-name"
echo ""
echo "脚本已生成到: $UPLOAD_DIR/github-upload"
echo "请执行: source ~/.bashrc (或 ~/.zshrc)"
echo "然后使用 github-upload 命令"
