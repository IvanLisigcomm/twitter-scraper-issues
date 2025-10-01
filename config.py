#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
"""

import os
from typing import Tuple

# 默认配置
DEFAULT_CONFIG = {
    'max_tweets': 50,
    'headless': False,
    'delay_range': (2, 5),
    'save_format': 'csv',
    'output_directory': './data',
    'window_size': (1920, 1080),
    'scroll_attempts': 10,
    'page_load_timeout': 20
}

def get_config() -> dict:
    """获取配置"""
    config = DEFAULT_CONFIG.copy()
    
    # 从环境变量读取配置（如果存在）
    if os.getenv('DEFAULT_MAX_TWEETS'):
        config['max_tweets'] = int(os.getenv('DEFAULT_MAX_TWEETS'))
    
    if os.getenv('DEFAULT_HEADLESS'):
        config['headless'] = os.getenv('DEFAULT_HEADLESS').lower() == 'true'
    
    if os.getenv('DEFAULT_DELAY_MIN') and os.getenv('DEFAULT_DELAY_MAX'):
        config['delay_range'] = (
            float(os.getenv('DEFAULT_DELAY_MIN')),
            float(os.getenv('DEFAULT_DELAY_MAX'))
        )
    
    if os.getenv('DEFAULT_SAVE_FORMAT'):
        config['save_format'] = os.getenv('DEFAULT_SAVE_FORMAT')
    
    if os.getenv('OUTPUT_DIRECTORY'):
        config['output_directory'] = os.getenv('OUTPUT_DIRECTORY')
    
    return config
