# 📖 使用示例

## 示例1：爬取Elon Musk的推文

### Web界面操作
1. 启动服务：`./start_web.sh`
2. 访问：http://localhost:8887
3. 填写表单：
   - 用户名：`elonmusk`
   - 数量：`50`
   - 格式：`csv`（默认）
   - 无头模式：`✓`
4. 点击"开始爬取"
5. 等待进度完成
6. 点击"预览数据"查看结果（支持CSV预览）
7. 点击"下载文件"保存到本地

### 预期结果
- 生成文件：`elonmusk_20251001_120000.json`
- 生成文件：`elonmusk_20251001_120000.csv`
- 包含最新50条推文
- 包含点赞、转发、评论数

## 示例2：批量爬取多个用户

### 方法A：Web界面连续操作
1. 爬取用户A
2. 等待完成
3. 点击"新建任务"
4. 爬取用户B
5. 重复步骤

### 方法B：命令行脚本
```bash
# 创建批量脚本
cat > batch_scrape.py << 'EOF'
from twitter_scraper import TwitterScraper

users = ['elonmusk', 'BillGates', 'BarackObama']
scraper = TwitterScraper(headless=True)

for user in users:
    print(f"开始爬取 {user}...")
    tweets = scraper.scrape_user_tweets(user, max_tweets=30)
    scraper.save_to_json()
    scraper.save_to_csv()
    print(f"{user} 完成！")

scraper.close()
EOF

python3 batch_scrape.py
```

## 示例3：查看历史数据

### Web界面
1. 访问首页
2. 滚动到"历史记录"区域
3. 点击刷新按钮
4. 查看所有已爬取的文件
5. 点击"预览"查看内容
6. 点击"下载"获取文件

### 命令行
```bash
# 查看所有JSON文件
ls -lh data/*.json

# 使用jq查看JSON内容（需安装jq）
cat data/elonmusk_*.json | jq '.[0]'

# 在Excel中打开CSV
open data/elonmusk_*.csv
```

## 示例4：数据分析

### 使用Python分析
```python
import json
import pandas as pd

# 读取JSON数据
with open('data/elonmusk_20251001_120000.json', 'r', encoding='utf-8') as f:
    tweets = json.load(f)

# 转换为DataFrame
df = pd.DataFrame(tweets)

# 分析统计
print(f"总推文数: {len(df)}")
print(f"平均点赞数: {df['likes'].mean():.0f}")
print(f"最受欢迎的推文: {df.loc[df['likes'].idxmax(), 'text'][:100]}...")

# 按时间分组
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
daily_tweets = df.groupby('date').size()
print("\n每日推文数量:")
print(daily_tweets)
```

### 使用Excel分析
1. 打开CSV文件
2. 使用筛选功能
3. 创建数据透视表
4. 生成图表

## 示例5：API调用

### 使用curl
```bash
# 开始爬取
curl -X POST http://localhost:8887/api/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "username": "elonmusk",
    "max_tweets": 20,
    "headless": true,
    "save_format": "csv"
  }'

# 查看状态
curl http://localhost:8887/api/status

# 获取历史记录
curl http://localhost:8887/api/history

# 预览CSV文件
curl http://localhost:8887/api/preview/elonmusk_20251001_120000.csv

# 下载文件
curl -O http://localhost:8887/api/download/elonmusk_20251001_120000.csv
```

### 使用Python requests
```python
import requests
import time

# 开始爬取
response = requests.post('http://localhost:8887/api/scrape', json={
    'username': 'elonmusk',
    'max_tweets': 50,
    'headless': True,
    'save_format': 'csv'  # 默认CSV格式
})

print(response.json())

# 轮询状态
while True:
    status = requests.get('http://localhost:8887/api/status').json()
    print(f"进度: {status['progress']}% - {status['status_message']}")
    
    if not status['is_running']:
        print("完成！")
        break
    
    time.sleep(2)

# 预览和下载文件
for file in status['output_files']:
    filename = file['name']
    
    # 预览文件（支持CSV和JSON）
    preview = requests.get(f'http://localhost:8887/api/preview/{filename}').json()
    print(f"预览 {filename}: {preview['total']}条推文")
    
    # 下载文件
    with open(filename, 'wb') as f:
        f.write(requests.get(f'http://localhost:8887/api/download/{filename}').content)
    print(f"已下载: {filename}")
```

## 示例6：定时任务

### 使用cron（Linux/Mac）
```bash
# 编辑crontab
crontab -e

# 每天凌晨2点爬取
0 2 * * * cd /path/to/推特爬虫 && python3 twitter_scraper.py < input.txt

# input.txt内容：
# elonmusk
# 100
# y
# both
```

### 使用Python schedule
```python
import schedule
import time
from twitter_scraper import TwitterScraper

def daily_scrape():
    print("开始每日爬取...")
    scraper = TwitterScraper(headless=True)
    tweets = scraper.scrape_user_tweets('elonmusk', max_tweets=50)
    scraper.save_to_json()
    scraper.save_to_csv()
    scraper.close()
    print("每日爬取完成！")

# 每天上午10点执行
schedule.every().day.at("10:00").do(daily_scrape)

print("定时任务已启动...")
while True:
    schedule.run_pending()
    time.sleep(60)
```

## 示例7：错误处理

### 处理网络错误
```python
from twitter_scraper import TwitterScraper
import time

scraper = TwitterScraper(headless=True)

max_retries = 3
for attempt in range(max_retries):
    try:
        tweets = scraper.scrape_user_tweets('elonmusk', max_tweets=50)
        if tweets:
            scraper.save_to_json()
            print("成功！")
            break
    except Exception as e:
        print(f"尝试 {attempt + 1} 失败: {e}")
        if attempt < max_retries - 1:
            print("等待30秒后重试...")
            time.sleep(30)
        else:
            print("所有尝试均失败")

scraper.close()
```

## 示例8：自定义配置

### 修改默认参数
```python
from twitter_scraper import TwitterScraper

# 自定义配置
scraper = TwitterScraper(
    headless=True,
    delay_range=(3, 8)  # 增加延迟避免被检测
)

# 爬取更多推文
tweets = scraper.scrape_user_tweets(
    username='elonmusk',
    max_tweets=200  # 更多推文
)

scraper.save_to_json()
scraper.close()
```

## 常见问题和解决方案

### Q1: 爬取速度慢？
```python
# A: 减少延迟（风险更高）
scraper = TwitterScraper(delay_range=(1, 3))
```

### Q2: 被检测到？
```python
# A: 增加延迟和随机性
scraper = TwitterScraper(delay_range=(5, 10))
```

### Q3: 内存占用高？
```python
# A: 分批处理
for i in range(0, 500, 50):
    tweets = scraper.scrape_user_tweets('user', max_tweets=50)
    scraper.save_to_json(f'batch_{i}.json')
    scraper.tweets_data.clear()  # 清空数据
```

### Q4: 需要代理？
```python
# A: 修改 twitter_scraper.py 添加代理支持
chrome_options.add_argument('--proxy-server=http://proxy:port')
```

## 最佳实践

1. **从少量开始**：先测试10-20条推文
2. **使用无头模式**：生产环境使用无头模式
3. **合理延迟**：设置3-6秒延迟避免被检测
4. **错误重试**：添加重试机制处理网络问题
5. **定期备份**：定期备份data目录
6. **监控日志**：记录爬取日志便于调试
7. **遵守规则**：遵守Twitter服务条款

---

更多示例和问题，请参考 README.md 文档。

