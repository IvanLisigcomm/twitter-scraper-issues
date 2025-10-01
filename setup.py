#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装脚本
"""

import subprocess
import sys
import os

def install_requirements():
    """安装依赖包"""
    print("正在安装Python依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包安装成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False

def create_output_directory():
    """创建输出目录"""
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✅ 创建输出目录: {output_dir}")
    else:
        print(f"✅ 输出目录已存在: {output_dir}")

def main():
    """主安装函数"""
    print("=== X（推特）推文爬虫 - 环境设置 ===")
    print()
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        return False
    
    print(f"✅ Python版本: {sys.version}")
    
    # 安装依赖
    if not install_requirements():
        return False
    
    # 创建输出目录
    create_output_directory()
    
    print()
    print("🎉 环境设置完成！")
    print("现在可以运行: python twitter_scraper.py")
    
    return True

if __name__ == "__main__":
    main()
