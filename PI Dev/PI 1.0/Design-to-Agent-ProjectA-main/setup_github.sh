#!/bin/bash

echo "=== GitHub 一键推送配置脚本 ==="

# 1. 配置 Git 用户信息
read -p "请输入你的 Git 用户名: " git_name
read -p "请输入你的 Git 邮箱: " git_email
git config --global user.name "$git_name"
git config --global user.email "$git_email"
echo "Git 用户信息配置完成。"

# 2. 生成 SSH 密钥（如果不存在）
SSH_KEY="$HOME/.ssh/id_ed25519"
if [ ! -f "$SSH_KEY" ]; then
    echo "正在生成 SSH 密钥..."
    ssh-keygen -t ed25519 -C "$git_email" -f "$SSH_KEY" -N ""
    echo "SSH 密钥已生成。"
else
    echo "SSH 密钥已存在，跳过生成。"
fi

# 3. 显示公钥（需手动添加到 GitHub）
echo ""
echo "请复制以下公钥内容，登录 GitHub 后前往 Settings → SSH and GPG keys → New SSH key 添加："
echo "----------------------------------------"
cat "${SSH_KEY}.pub"
echo "----------------------------------------"

# 4. 测试 SSH 连接提示
echo ""
echo "添加公钥后，请在终端运行以下命令测试连接："
echo "ssh -T git@github.com"

# 5. 仓库初始化与推送准备提示
echo ""
echo "在你的项目目录下运行以下命令完成推送："
echo "git init"
echo "git remote add origin git@github.com:你的用户名/仓库名.git"
echo "git add ."
echo "git commit -m \"初始提交\""
echo "git push -u origin main"

echo ""
echo "配置完成！后续只需在项目目录执行 git push 即可。"
