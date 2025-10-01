#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter爬虫 Web 应用
提供Web界面和API接口来使用爬虫功能
"""

import os
import json
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from twitter_scraper import TwitterScraper
import time

app = Flask(__name__)
CORS(app)

# 全局变量用于追踪爬取状态
scraping_status = {
    'is_running': False,
    'progress': 0,
    'current_tweets': 0,
    'target_tweets': 0,
    'status_message': '',
    'username': '',
    'error': None,
    'output_files': []
}

def background_scraper(username, max_tweets, headless, save_format):
    """后台爬取任务"""
    global scraping_status
    
    try:
        scraping_status['is_running'] = True
        scraping_status['progress'] = 0
        scraping_status['current_tweets'] = 0
        scraping_status['target_tweets'] = max_tweets
        scraping_status['username'] = username
        scraping_status['status_message'] = '正在初始化浏览器...'
        scraping_status['error'] = None
        scraping_status['output_files'] = []
        
        # 创建爬虫实例
        scraper = TwitterScraper(headless=headless)
        
        # 自定义进度回调
        def update_progress(current, total, message):
            scraping_status['current_tweets'] = current
            scraping_status['target_tweets'] = total
            scraping_status['progress'] = int((current / total) * 100) if total > 0 else 0
            scraping_status['status_message'] = message
        
        scraping_status['status_message'] = '正在爬取推文...'
        
        # 爬取推文
        tweets = scraper.scrape_user_tweets(username, max_tweets)
        
        if tweets:
            scraping_status['status_message'] = '正在保存数据...'
            scraping_status['current_tweets'] = len(tweets)
            scraping_status['progress'] = 100
            
            # 保存文件
            output_files = []
            if save_format in ['json', 'both']:
                json_file = scraper.save_to_json()
                output_files.append({'type': 'json', 'path': json_file, 'name': os.path.basename(json_file)})
            
            if save_format in ['csv', 'both']:
                csv_file = scraper.save_to_csv()
                output_files.append({'type': 'csv', 'path': csv_file, 'name': os.path.basename(csv_file)})
            
            scraping_status['output_files'] = output_files
            scraping_status['status_message'] = f'完成！成功爬取 {len(tweets)} 条推文'
        else:
            scraping_status['error'] = '未能爬取到任何推文'
            scraping_status['status_message'] = '爬取失败'
        
        scraper.close()
        
    except Exception as e:
        scraping_status['error'] = str(e)
        scraping_status['status_message'] = f'错误: {str(e)}'
    finally:
        scraping_status['is_running'] = False


@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')


@app.route('/api/scrape', methods=['POST'])
def start_scraping():
    """开始爬取API"""
    global scraping_status
    
    # 检查是否已有任务在运行
    if scraping_status['is_running']:
        return jsonify({'error': '已有爬取任务在运行中'}), 400
    
    data = request.json
    username = data.get('username', '').strip()
    max_tweets = int(data.get('max_tweets', 50))
    headless = data.get('headless', True)
    save_format = data.get('save_format', 'json')
    
    if not username:
        return jsonify({'error': '用户名不能为空'}), 400
    
    # 启动后台线程
    thread = threading.Thread(
        target=background_scraper,
        args=(username, max_tweets, headless, save_format)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': '爬取任务已启动', 'username': username})


@app.route('/api/status', methods=['GET'])
def get_status():
    """获取爬取状态API"""
    return jsonify(scraping_status)


@app.route('/api/download/<filename>')
def download_file(filename):
    """下载文件API"""
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    filepath = os.path.join(data_dir, filename)
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({'error': '文件不存在'}), 404


@app.route('/api/preview/<filename>')
def preview_file(filename):
    """预览JSON/CSV文件API"""
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    filepath = os.path.join(data_dir, filename)
    
    if os.path.exists(filepath):
        try:
            if filename.endswith('.json'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 只返回前10条用于预览
                    return jsonify({'tweets': data[:10], 'total': len(data), 'format': 'json'})
            elif filename.endswith('.csv'):
                import csv
                tweets = []
                with open(filepath, 'r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    for i, row in enumerate(reader):
                        if i >= 10:  # 只读取前10条
                            break
                        tweets.append(row)
                
                # 计算总行数
                with open(filepath, 'r', encoding='utf-8-sig') as f:
                    total = sum(1 for line in f) - 1  # 减去表头
                
                return jsonify({'tweets': tweets, 'total': total, 'format': 'csv'})
            else:
                return jsonify({'error': '只支持预览JSON和CSV文件'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': '文件不存在'}), 404


@app.route('/api/history')
def get_history():
    """获取历史爬取记录"""
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    
    if not os.path.exists(data_dir):
        return jsonify({'files': []})
    
    files = []
    for filename in os.listdir(data_dir):
        if filename.endswith(('.json', '.csv')):
            filepath = os.path.join(data_dir, filename)
            stat = os.stat(filepath)
            files.append({
                'name': filename,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'type': 'JSON' if filename.endswith('.json') else 'CSV'
            })
    
    # 按修改时间排序（最新的在前）
    files.sort(key=lambda x: x['modified'], reverse=True)
    
    return jsonify({'files': files})


if __name__ == '__main__':
    print("=== Twitter爬虫 Web 应用 ===")
    print("启动服务器...")
    print("访问地址: http://localhost:8887")
    print("按 Ctrl+C 停止服务器")
    app.run(debug=True, host='0.0.0.0', port=8887)

