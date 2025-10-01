# 🐦 Twitter 推文爬虫 SaaS 平台

<div align="center">

![Version](https://img.shields.io/badge/version-2.1-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)

**一个功能强大、界面现代的 Twitter 推文数据采集平台**

[快速开始](#-快速开始) • [功能特性](#-功能特性) • [使用文档](#-使用文档) • [API文档](#-api文档)

</div>

---

## 📖 项目简介

这是一个基于 Python + Flask + Selenium 开发的 Twitter 推文爬虫系统，提供现代化的 Web 界面和强大的数据采集功能。支持实时进度追踪、在线数据预览、多格式导出等特性，让数据采集变得简单高效。

### 🎯 适用场景

- 📊 社交媒体数据分析
- 🔍 舆情监测与分析
- 📈 趋势研究
- 🎓 学术研究
- 💼 市场调研

---
<img width="2412" height="1094" alt="image" src="https://github.com/user-attachments/assets/fbecaeac-96ac-4285-85e2-812b8018f640" />

## ✨ 功能特性

### 🎨 现代化 Web 界面
- **深色主题设计**：现代化 SaaS 风格 UI
- **流畅动画效果**：渐变背景、卡片悬停、进度条动画
- **响应式布局**：完美支持桌面、平板、移动端
- **实时进度追踪**：可视化进度条，实时状态更新
- **在线数据预览**：支持 CSV 和 JSON 格式预览
- **历史记录管理**：查看和管理所有爬取记录

### 🤖 智能爬取引擎
- **反检测机制**：随机 User-Agent、禁用自动化标识
- **模拟人工行为**：随机延迟、智能滚动、自然操作
- **智能去重**：基于时间戳和内容的智能去重
- **自动重试**：网络错误自动重试（最多3次）
- **完整数据**：推文文本、时间、点赞、转发、评论数

### 📊 数据导出
- **CSV 格式**（默认）：Excel 可直接打开，UTF-8 BOM 编码
- **JSON 格式**：结构化数据，适合程序处理
- **批量导出**：支持同时保存两种格式
- **自动命名**：用户名_时间戳.格式

### 🔧 便捷部署
- **一键启动**：提供启动脚本（macOS/Linux/Windows）
- **自动配置**：ChromeDriver 自动下载和配置
- **无需数据库**：文件系统存储，简单可靠
- **跨平台支持**：Windows、macOS、Linux

---

## 🚀 快速开始

### 前置要求

- Python 3.7 或更高版本
- Chrome 浏览器（需预先安装）
- 稳定的网络连接

### 安装步骤

1. **克隆或下载项目**
```bash
cd twitter-scraper-issues
```

2. **安装依赖**
```bash
pip3 install -r requirements.txt
```

3. **启动 Web 服务**

**macOS/Linux:**
```bash
./start_web.sh
```

**Windows:**
```bash
start_web.bat
```

**或直接运行:**
```bash
python3 app.py
```

4. **访问 Web 界面**
```
打开浏览器访问: http://localhost:8887
```

就这么简单！🎉

---

## 💻 使用方法

### 方法一：Web 界面（推荐）

#### 基本使用流程

1. **访问首页**
   - 打开浏览器访问 `http://localhost:8887`
<img width="1448" height="1212" alt="image" src="https://github.com/user-attachments/assets/cb118766-53e0-419b-b9e7-1193dbb093a6" />   
2. **填写参数**
   - 用户名：输入 Twitter 用户名（不含 @ 符号）
   - 数量：设置爬取推文数量（1-1000）
   - 格式：选择保存格式（默认 CSV）
   - 无头模式：勾选后浏览器后台运行

4. **开始爬取**
   - 点击"开始爬取"按钮
   - 实时查看进度和状态

5. **查看结果**
   - 点击"预览数据"在线查看（支持 CSV 和 JSON）
   - 点击"下载文件"保存到本地
   - 在"历史记录"中管理所有文件

#### Web 界面特性

- ✅ 实时进度显示（百分比 + 统计）
- ✅ 在线预览前 10 条推文
- ✅ 格式标签识别（CSV/JSON）
- ✅ 历史记录一键预览/下载
- ✅ 移动端完美适配

### 方法二：命令行

```bash
python3 twitter_scraper.py
```

按照提示输入：
- 用户名
- 爬取数量
- 是否无头模式
- 保存格式（默认 CSV）

### 方法三：Python 代码

```python
from twitter_scraper import TwitterScraper

# 创建爬虫实例
scraper = TwitterScraper(
    headless=True,           # 无头模式
    delay_range=(3, 6)       # 延迟范围
)

try:
    # 爬取推文
    tweets = scraper.scrape_user_tweets(
        username='elonmusk',
        max_tweets=100
    )
    
    # 保存数据
    scraper.save_to_csv()    # CSV 格式
    # scraper.save_to_json() # JSON 格式
    
    print(f"成功爬取 {len(tweets)} 条推文")
    
finally:
    scraper.close()
```

---

## 📋 API 文档

### REST API 接口

Web 应用提供以下 API 接口：

#### 1. 开始爬取

```http
POST /api/scrape
Content-Type: application/json

{
  "username": "elonmusk",
  "max_tweets": 50,
  "headless": true,
  "save_format": "csv"  // json | csv | both
}
```

**响应:**
```json
{
  "message": "爬取任务已启动",
  "username": "elonmusk"
}
```

#### 2. 获取爬取状态

```http
GET /api/status
```

**响应:**
```json
{
  "is_running": true,
  "progress": 60,
  "current_tweets": 30,
  "target_tweets": 50,
  "status_message": "正在爬取推文...",
  "username": "elonmusk",
  "error": null,
  "output_files": []
}
```

#### 3. 预览数据

```http
GET /api/preview/<filename>
```

支持预览 CSV 和 JSON 文件，返回前 10 条数据。

**响应:**
```json
{
  "tweets": [...],
  "total": 50,
  "format": "csv"
}
```

#### 4. 下载文件

```http
GET /api/download/<filename>
```

下载指定文件。

#### 5. 获取历史记录

```http
GET /api/history
```

**响应:**
```json
{
  "files": [
    {
      "name": "elonmusk_20251001_120000.csv",
      "size": 12345,
      "modified": "2025-10-01T12:00:00",
      "type": "CSV"
    }
  ]
}
```

### API 使用示例

#### curl 示例

```bash
# 开始爬取
curl -X POST http://localhost:8887/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"username": "elonmusk", "max_tweets": 20, "headless": true, "save_format": "csv"}'

# 查看状态
curl http://localhost:8887/api/status

# 预览数据
curl http://localhost:8887/api/preview/elonmusk_20251001_120000.csv
```

#### Python 示例

```python
import requests
import time

# 开始爬取
response = requests.post('http://localhost:8887/api/scrape', json={
    'username': 'elonmusk',
    'max_tweets': 50,
    'headless': True,
    'save_format': 'csv'
})

# 轮询状态
while True:
    status = requests.get('http://localhost:8887/api/status').json()
    print(f"进度: {status['progress']}%")
    if not status['is_running']:
        break
    time.sleep(2)

# 下载文件
for file in status['output_files']:
    with open(file['name'], 'wb') as f:
        content = requests.get(f'http://localhost:8887/api/download/{file["name"]}').content
        f.write(content)
```

---

## 📁 项目结构

```
推特爬虫/
├── app.py                      # Flask Web 应用
├── twitter_scraper.py          # 爬虫核心引擎
├── config.py                   # 配置文件
├── requirements.txt            # Python 依赖
├── setup.py                    # 安装脚本
├── start_web.sh               # 启动脚本（Unix）
├── start_web.bat              # 启动脚本（Windows）
├── run.sh                     # 命令行脚本
├── README.md                  # 项目文档（本文件）
│
├── templates/                 # HTML 模板
│   └── index.html            # Web 界面主页
│
├── static/                    # 静态资源
│   ├── css/
│   │   └── style.css         # 样式文件
│   └── js/
│       └── main.js           # JavaScript 逻辑
│
├── data/                      # 数据输出目录
│   ├── *.csv                 # CSV 格式数据
│   └── *.json                # JSON 格式数据
│
└── docs/                      # 文档目录
    ├── QUICKSTART.md         # 快速入门
    ├── START_HERE.md         # 新手指南
    ├── USAGE_EXAMPLES.md     # 使用示例
    ├── DEMO_GUIDE.md         # 界面说明
    ├── PROJECT_SUMMARY.md    # 项目总结
    ├── CSV_PREVIEW_FEATURE.md # CSV 预览功能
    ├── PORT_FIX.md           # 端口配置
    ├── CHANGELOG.md          # 更新日志
    └── DOCS_UPDATE_SUMMARY.md # 文档更新
```

---

## 🛠️ 技术栈

### 后端技术
- **Flask 3.0.0** - Web 框架
- **Flask-CORS 4.0.0** - 跨域支持
- **Selenium 4.15.2** - 浏览器自动化
- **BeautifulSoup4 4.12.2** - HTML 解析
- **webdriver-manager 4.0.1** - ChromeDriver 管理
- **fake-useragent 1.4.0** - User-Agent 生成

### 前端技术
- **HTML5** - 语义化标签
- **CSS3** - 现代布局和动画
  - CSS Grid & Flexbox
  - CSS 变量
  - 动画和过渡效果
  - 渐变背景
- **JavaScript (ES6+)** - 交互逻辑
  - Fetch API
  - 异步编程
  - DOM 操作
- **Font Awesome 6.4.0** - 图标库

---

## ⚙️ 配置选项

### 环境变量（可选）

创建 `.env` 文件配置默认值：

```bash
DEFAULT_MAX_TWEETS=100
DEFAULT_HEADLESS=true
DEFAULT_DELAY_MIN=2
DEFAULT_DELAY_MAX=5
DEFAULT_SAVE_FORMAT=csv
OUTPUT_DIRECTORY=./data
```

### 自定义配置

编辑 `config.py` 修改默认配置：

```python
DEFAULT_CONFIG = {
    'max_tweets': 50,
    'headless': False,
    'delay_range': (2, 5),
    'save_format': 'csv',      # json | csv | both
    'output_directory': './data',
    'window_size': (1920, 1080),
    'scroll_attempts': 10,
    'page_load_timeout': 20
}
```

### 修改端口

编辑 `app.py` 最后一行：

```python
app.run(debug=True, host='0.0.0.0', port=8887)  # 改为其他端口
```

---

## 📊 数据格式

### CSV 格式（默认）

```csv
text,timestamp,time_display,likes,retweets,replies,scraped_at
"推文内容...",2025-01-01T12:00:00Z,2小时,1234,567,89,2025-01-01T14:00:00
```

**字段说明：**
- `text`: 推文文本内容
- `timestamp`: ISO 格式时间戳
- `time_display`: 显示的相对时间
- `likes`: 点赞数
- `retweets`: 转发数
- `replies`: 评论数
- `scraped_at`: 爬取时间

**特点：**
- ✅ UTF-8 BOM 编码
- ✅ Excel 可直接打开
- ✅ 中文完美显示
- ✅ 适合数据分析

### JSON 格式

```json
[
  {
    "text": "推文内容...",
    "timestamp": "2025-01-01T12:00:00Z",
    "time_display": "2小时",
    "likes": 1234,
    "retweets": 567,
    "replies": 89,
    "scraped_at": "2025-01-01T14:00:00"
  }
]
```

**特点：**
- ✅ 结构化数据
- ✅ 程序易处理
- ✅ 支持嵌套
- ✅ 2空格缩进

---

## 🔍 常见问题

### Q1: 页面无法访问？

**A:** 检查端口是否被占用
```bash
lsof -i :8887
```
如果被占用，修改 `app.py` 中的端口号。

### Q2: ChromeDriver 错误？

**A:** 确保：
- ✅ Chrome 浏览器已安装
- ✅ 网络连接正常（首次需下载驱动）
- ✅ 删除 `~/.wdm` 缓存重试

### Q3: 爬取数量不足？

**原因：**
- 用户推文数量本身不足
- 已到达页面底部
- 网络延迟导致加载慢

**解决：**
- 增加延迟时间
- 检查用户推文数量
- 使用非无头模式观察

### Q4: CSV 文件乱码？

**A:** 程序已使用 UTF-8 BOM 编码，Excel 应能自动识别。
如仍有问题：
1. Excel → 数据 → 从文本/CSV
2. 选择 UTF-8 编码导入

### Q5: 找不到推文元素？

**A:** Twitter 更新了页面结构，需要：
1. 使用非无头模式查看页面
2. 更新 CSS 选择器
3. 检查网络连接

### Q6: 如何设置代理？

**A:** 修改 `twitter_scraper.py` 的 `setup_driver` 方法：
```python
chrome_options.add_argument('--proxy-server=http://proxy:port')
```

---

## ⚠️ 注意事项

### 使用限制

- ⚠️ **仅供学习研究使用**
- 🚫 **请勿用于商业用途**
- 🚫 **请勿用于大规模数据采集**
- ⚠️ **请遵守 Twitter 服务条款**
- ⏰ **合理控制爬取频率**

### 技术限制

- 需要稳定的网络连接
- 可能因 Twitter 反爬机制失效
- 页面结构变化可能影响数据提取
- ChromeDriver 需要与 Chrome 版本匹配

### 法律声明

使用本工具产生的所有后果由使用者自行承担。作者不对使用本工具产生的任何后果承担责任。

---

## 📈 性能建议

### 爬取速度

| 推文数量 | 预计时间 | 建议配置 |
|---------|---------|---------|
| < 50 | 1-3分钟 | delay=(2,5), headless=False |
| 50-100 | 3-6分钟 | delay=(2,5), headless=True |
| 100-500 | 10-30分钟 | delay=(3,6), headless=True |
| > 500 | 30分钟+ | delay=(4,8), headless=True |

### 优化建议

1. **小规模测试**：先爬取 10-20 条测试
2. **使用无头模式**：生产环境建议使用
3. **合理设置延迟**：3-6 秒避免被检测
4. **网络稳定性**：确保网络连接良好
5. **分批处理**：大量数据建议分批爬取

---

## 📚 使用文档

### 新手入门
- 📖 [START_HERE.md](START_HERE.md) - 从这里开始
- 🚀 [QUICKSTART.md](QUICKSTART.md) - 快速入门指南

### 功能说明
- 💡 [CSV_PREVIEW_FEATURE.md](CSV_PREVIEW_FEATURE.md) - CSV 预览功能
- 🎨 [DEMO_GUIDE.md](DEMO_GUIDE.md) - 界面演示说明
- 🔧 [PORT_FIX.md](PORT_FIX.md) - 端口配置说明

### 使用示例
- 📋 [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - 详细使用示例
- 🏗️ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目技术总结

### 更新记录
- 📝 [CHANGELOG.md](CHANGELOG.md) - 版本更新日志
- 📚 [DOCS_UPDATE_SUMMARY.md](DOCS_UPDATE_SUMMARY.md) - 文档更新总结

---

## 🔄 版本历史

### v2.1 (2025-10-01) - 当前版本 ✨

**新增功能：**
- ✅ CSV 文件在线预览
- ✅ 格式标签显示（CSV/JSON）
- ✅ 默认保存格式改为 CSV
- ✅ 端口优化为 8887

**改进：**
- ✅ 预览优先查找 CSV 文件
- ✅ 历史记录所有文件可预览
- ✅ API 支持 CSV 和 JSON 预览
- ✅ 统一预览界面体验

### v2.0 (2025-10-01)

**全新 Web 界面：**
- ✨ 现代化 SaaS 风格 UI
- ✨ 实时进度追踪
- ✨ 数据在线预览（JSON）
- ✨ 历史记录管理
- ✨ REST API 接口
- ✨ 响应式设计
- ✨ 流畅动画效果

### v1.0 (2025-09-27)

**初始版本：**
- ✨ 基本推文爬取功能
- ✨ 反检测机制
- ✨ JSON 和 CSV 双格式
- ✨ 自动 ChromeDriver 管理
- ✨ 智能去重
- ✨ 错误处理和重试

完整更新日志请查看 [CHANGELOG.md](CHANGELOG.md)

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 如何贡献

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 问题反馈

- 📝 提交 Issue 描述问题
- 🔧 提供复现步骤
- 💬 参与讨论

---

## 📄 开源协议

本项目采用 MIT 协议开源。

**MIT License**

```
Copyright (c) 2025 Twitter Scraper Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🌟 Star History

如果这个项目对你有帮助，请给它一个 ⭐ Star！

---

## 📞 联系方式

- 📧 Email: spaciousli2025@gmail.com
- 💬 Issues: [GitHub Issues](https://github.com/IvanLisigcomm/twitter-scraper/issues)


---

## 🎉 致谢

感谢以下开源项目：

- [Selenium](https://www.selenium.dev/) - 浏览器自动化
- [Flask](https://flask.palletsprojects.com/) - Web 框架
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML 解析
- [Font Awesome](https://fontawesome.com/) - 图标库

---

<div align="center">

**⭐ 如果觉得有用，请给个 Star ⭐**

**Made with ❤️ by Twitter Scraper Team**

[返回顶部](#-twitter-推文爬虫-saas-平台)

</div>

