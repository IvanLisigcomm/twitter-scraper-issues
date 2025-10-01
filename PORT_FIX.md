# 🔧 端口配置说明

## 当前配置

**项目使用端口：8887**

访问地址：**http://localhost:8887**

### 为什么选择8887？

1. ❌ 5000端口 - macOS系统AirPlay Receiver服务占用
2. ❌ 8080端口 - 常被其他Web服务占用
3. ✅ 8887端口 - 通常可用，避免常见冲突

---

## 🚀 启动方式

### 方法一：使用启动脚本
```bash
./start_web.sh
```
访问：http://localhost:8887

### 方法二：直接运行
```bash
python3 app.py
```
访问：http://localhost:8887

---

## 🔧 其他解决方案

### 方案1：关闭macOS AirPlay Receiver（不推荐）

1. 打开"系统设置"（System Settings）
2. 进入"通用"（General）
3. 找到"AirDrop与接力"（AirDrop & Handoff）
4. 关闭"AirPlay接收器"（AirPlay Receiver）

### 方案2：使用不同端口（推荐）

修改 `app.py` 最后一行的端口号：

```python
# 当前配置（8887端口）
app.run(debug=True, host='0.0.0.0', port=8887)

# 可改为其他端口
app.run(debug=True, host='0.0.0.0', port=3000)
app.run(debug=True, host='0.0.0.0', port=8000)
app.run(debug=True, host='0.0.0.0', port=8888)
```

### 方案3：查找占用端口的进程

```bash
# 查看什么占用了8887端口
lsof -i :8887

# 如果需要关闭该进程
kill -9 <PID>
```

---

## 📝 常用端口推荐

如果8887也被占用，可以尝试以下端口：

- **8887** ✅ 当前使用
- **3000** - 常用于Node.js项目
- **8000** - 常用于Python项目
- **8888** - Jupyter常用端口
- **9000** - 通常可用
- **7000** - 备选端口

---

## 🔍 检查端口是否可用

```bash
# 检查端口是否被占用
lsof -i :8887

# 如果没有输出，说明端口可用
```

---

## ✅ 验证配置

运行以下命令确认服务正常：

```bash
# 启动服务
./start_web.sh

# 应该看到：
# 访问地址: http://localhost:8887
```

打开浏览器访问 http://localhost:8887 即可使用！

---

## 📚 相关文档

所有文档已更新为8887端口：
- ✅ app.py → 8887端口
- ✅ start_web.sh → 8887端口
- ✅ start_web.bat → 8887端口
- ✅ 所有Markdown文档 → 8887端口

---

## 🎉 端口历史

- v1.0: 无Web界面
- v2.0: 使用5000端口（macOS冲突）
- v2.0.1: 改为8080端口（仍有冲突）
- v2.1: 改为8887端口（当前版本，稳定）

---

**配置完成！享受使用！** 🎉

