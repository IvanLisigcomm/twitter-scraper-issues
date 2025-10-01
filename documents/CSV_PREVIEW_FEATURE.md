# 📊 CSV文件预览功能说明

## ✨ 新增功能

现在Web界面支持预览CSV格式的文件了！

### 🎯 功能特性

#### 1. **后端支持**
- ✅ API支持预览JSON和CSV两种格式
- ✅ 自动识别文件格式
- ✅ CSV使用UTF-8-sig编码读取（兼容Excel）
- ✅ 只加载前10条数据（性能优化）
- ✅ 返回总行数统计

#### 2. **前端增强**
- ✅ 优先预览CSV文件（因为现在默认格式是CSV）
- ✅ 如果没有CSV，自动查找JSON文件
- ✅ 预览界面显示格式标签（CSV/JSON）
- ✅ 统一的预览界面样式

#### 3. **历史记录**
- ✅ 所有文件（JSON和CSV）都显示预览按钮
- ✅ 点击预览按钮可以查看任何格式的文件
- ✅ 自动识别和处理不同格式

---

## 🚀 使用方法

### 方法一：爬取完成后预览

1. 完成爬取任务
2. 点击"预览数据"按钮
3. 系统会自动查找：
   - 先找CSV文件
   - 没有CSV则找JSON文件
4. 显示前10条推文内容

### 方法二：历史记录预览

1. 滚动到"历史记录"区域
2. 找到任何一个文件（CSV或JSON）
3. 点击"预览"按钮（眼睛图标）
4. 在弹出的对话框中查看内容

---

## 📋 预览界面

### 显示内容
- **格式标签**：显示文件格式（CSV或JSON）
- **统计信息**：显示前10条，共XX条推文
- **推文详情**：
  - 推文文本内容
  - ❤️ 点赞数
  - 🔄 转发数
  - 💬 评论数
  - ⏰ 发布时间

### 示例效果
```
[CSV] 显示前10条，共50条推文

┌─────────────────────────────────────┐
│ 推文内容文本...                      │
│ ❤️ 1.2K  🔄 234  💬 89  ⏰ 2小时     │
└─────────────────────────────────────┘
```

---

## 🔧 技术实现

### 后端（app.py）

```python
@app.route('/api/preview/<filename>')
def preview_file(filename):
    if filename.endswith('.csv'):
        import csv
        tweets = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 10:
                    break
                tweets.append(row)
        
        total = sum(1 for line in f) - 1
        return jsonify({'tweets': tweets, 'total': total, 'format': 'csv'})
```

### 前端（main.js）

```javascript
async function previewData() {
    // 优先查找CSV文件
    let fileToPreview = currentFiles.find(f => f.type === 'csv');
    if (!fileToPreview) {
        fileToPreview = currentFiles.find(f => f.type === 'json');
    }
    
    const response = await fetch(`/api/preview/${fileToPreview.name}`);
    const data = await response.json();
    displayPreview(data, fileToPreview.name);
}
```

---

## ✅ 支持的字段

CSV和JSON都支持以下字段：
- `text` - 推文文本
- `likes` - 点赞数
- `retweets` - 转发数
- `replies` - 评论数
- `time_display` - 显示时间
- `timestamp` - 完整时间戳
- `scraped_at` - 爬取时间

---

## 🎨 优势

### CSV预览的好处
1. **直观**：表格形式更适合数据查看
2. **兼容**：与Excel完全兼容
3. **轻量**：文件体积更小
4. **通用**：所有数据分析工具都支持

### 统一体验
- JSON和CSV使用相同的预览界面
- 自动格式识别
- 无需用户手动选择

---

## 📝 示例场景

### 场景1：快速查看数据
```
1. 爬取 @elonmusk 50条推文
2. 选择保存为CSV（默认）
3. 点击"预览数据"
4. 立即在浏览器中查看内容
5. 确认无误后下载
```

### 场景2：对比不同格式
```
1. 爬取同一用户，保存为"两种格式"
2. 在历史记录中看到两个文件
3. 分别预览CSV和JSON
4. 选择最适合的格式下载
```

### 场景3：历史数据查看
```
1. 打开历史记录
2. 找到之前爬取的CSV文件
3. 点击预览快速查看内容
4. 无需下载即可确认数据
```

---

## 🔍 数据格式对比

### CSV格式
```csv
text,timestamp,time_display,likes,retweets,replies,scraped_at
"推文内容...",2025-01-01T12:00:00Z,2小时,1234,567,89,2025-01-01T14:00:00
```

### JSON格式
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

两种格式在预览界面中显示效果完全一致！

---

## ⚡ 性能优化

1. **按需加载**：只加载前10条数据
2. **快速计数**：高效计算总行数
3. **流式读取**：不会一次性加载整个文件
4. **缓存友好**：重复预览不会重新读取

---

## 🎉 总结

现在你可以：
- ✅ 预览CSV文件内容
- ✅ 预览JSON文件内容
- ✅ 在线查看推文数据
- ✅ 无需下载即可确认内容
- ✅ 支持历史记录预览
- ✅ 自动格式识别

**享受更便捷的数据预览体验吧！** 🚀

