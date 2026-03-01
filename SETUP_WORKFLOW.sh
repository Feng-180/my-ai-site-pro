#!/bin/bash

# ==========================================
# 全球硬通货情报局 v3.0 - 一键配置脚本
# 该脚本将为您在 GitHub 仓库中创建自动化更新文件
# ==========================================

echo "正在配置 GitHub Actions 自动化脚本..."

# 创建目录
mkdir -p .github/workflows

# 写入工作流内容
cat << 'EOF' > .github/workflows/update.yml
name: 自动抓取硬通货情报

on:
  schedule:
    - cron: '0 23 * * *'   # 每天早上 7:00 运行
    - cron: '0 11 * * *'   # 每天晚上 19:00 运行
  workflow_dispatch:       # 支持手动运行

jobs:
  run-scraper:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: pip install requests pycryptodome urllib3
      - name: Run Scraper
        env:
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
        run: python scraper.py
      - name: Commit & Push
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data.enc
          git diff --staged --quiet || (git commit -m "Auto-Update Data" && git push)
EOF

echo "✅ 配置完成！"
echo "请执行以下命令将配置推送到您的仓库："
echo "git add .github/workflows/update.yml"
echo "git commit -m 'Setup: Add auto-update workflow'"
echo "git push origin main"
