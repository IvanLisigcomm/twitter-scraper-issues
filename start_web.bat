@echo off
REM Twitter爬虫 Web应用启动脚本 (Windows)

echo ================================
echo   Twitter爬虫 Web应用启动脚本
echo ================================
echo.

REM 检查Python
echo 检查Python版本...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python
    pause
    exit /b 1
)

python --version
echo.

REM 检查依赖
echo 检查依赖...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo 未安装Flask，正在安装依赖...
    python -m pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo 依赖安装完成
    ) else (
        echo 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo 依赖已安装
)
echo.

REM 创建必要的目录
echo 检查目录结构...
if not exist "data" mkdir data
if not exist "templates" mkdir templates
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
echo 目录结构正常
echo.

REM 启动Flask应用
echo ================================
echo 启动Web服务器...
echo ================================
echo.
echo 访问地址: http://localhost:8080
echo 按 Ctrl+C 停止服务器
echo 提示: 如果端口被占用，可以修改 app.py 中的端口号
echo.

python app.py
pause

