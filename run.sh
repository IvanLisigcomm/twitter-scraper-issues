#!/bin/bash
# X（推特）推文爬虫启动脚本

echo "=== X（推特）推文爬虫启动脚本 ==="
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

# 检查是否已安装依赖
if [ ! -f "requirements.txt" ]; then
    echo "❌ 未找到requirements.txt文件"
    exit 1
fi

# 创建输出目录
mkdir -p output

echo "正在检查依赖包..."
python3 -c "import selenium, bs4, pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "正在安装依赖包..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖包安装失败"
        exit 1
    fi
fi

echo "✅ 环境检查完成"
echo

# 运行主程序
python3 twitter_scraper.py
