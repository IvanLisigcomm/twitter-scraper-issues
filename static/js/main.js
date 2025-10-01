// ========== 全局变量 ==========
let statusCheckInterval = null;
let currentFiles = [];

// ========== 初始化 ==========
document.addEventListener('DOMContentLoaded', function() {
    // 加载历史记录
    loadHistory();
    
    // 设置导航链接
    setupNavigation();
    
    // 设置平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// ========== 导航设置 ==========
function setupNavigation() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });
}

// ========== 滚动到表单 ==========
function scrollToForm() {
    const scraperSection = document.getElementById('scraper');
    scraperSection.scrollIntoView({ behavior: 'smooth' });
}

// ========== 开始爬取 ==========
async function startScraping() {
    const username = document.getElementById('username').value.trim();
    const maxTweets = parseInt(document.getElementById('maxTweets').value);
    const saveFormat = document.getElementById('saveFormat').value;
    const headless = document.getElementById('headless').checked;
    
    // 验证输入
    if (!username) {
        showNotification('请输入用户名', 'error');
        return;
    }
    
    if (maxTweets < 1 || maxTweets > 1000) {
        showNotification('推文数量必须在1-1000之间', 'error');
        return;
    }
    
    // 隐藏表单，显示进度
    document.getElementById('scraperForm').style.display = 'none';
    document.getElementById('progressContainer').style.display = 'block';
    document.getElementById('currentUsername').textContent = username;
    
    try {
        const response = await fetch('/api/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                max_tweets: maxTweets,
                headless: headless,
                save_format: saveFormat
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // 开始轮询状态
            startStatusPolling();
        } else {
            showNotification(data.error || '启动失败', 'error');
            resetForm();
        }
    } catch (error) {
        showNotification('网络错误: ' + error.message, 'error');
        resetForm();
    }
}

// ========== 状态轮询 ==========
function startStatusPolling() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }
    
    statusCheckInterval = setInterval(async () => {
        try {
            const response = await fetch('/api/status');
            const status = await response.json();
            
            updateProgress(status);
            
            // 如果完成或出错，停止轮询
            if (!status.is_running) {
                clearInterval(statusCheckInterval);
                statusCheckInterval = null;
                
                if (status.error) {
                    showNotification('爬取失败: ' + status.error, 'error');
                } else if (status.output_files && status.output_files.length > 0) {
                    currentFiles = status.output_files;
                    document.getElementById('actionButtons').style.display = 'grid';
                    showNotification('爬取完成！', 'success');
                    // 刷新历史记录
                    loadHistory();
                }
            }
        } catch (error) {
            console.error('获取状态失败:', error);
        }
    }, 1000);
}

// ========== 更新进度显示 ==========
function updateProgress(status) {
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const currentTweets = document.getElementById('currentTweets');
    const targetTweets = document.getElementById('targetTweets');
    const statusMessage = document.getElementById('statusMessage');
    const progressStatus = document.getElementById('progressStatus');
    
    // 更新进度条
    const progress = status.progress || 0;
    progressBar.style.width = progress + '%';
    progressText.textContent = progress + '%';
    
    // 更新统计
    currentTweets.textContent = status.current_tweets || 0;
    targetTweets.textContent = status.target_tweets || 0;
    
    // 更新状态消息
    statusMessage.querySelector('span').textContent = status.status_message || '处理中...';
    
    // 更新状态标签
    if (status.is_running) {
        progressStatus.textContent = '爬取中...';
        progressStatus.style.background = 'rgba(29, 161, 242, 0.1)';
        progressStatus.style.color = '#1DA1F2';
    } else if (status.error) {
        progressStatus.textContent = '失败';
        progressStatus.style.background = 'rgba(249, 24, 128, 0.1)';
        progressStatus.style.color = '#f91880';
    } else {
        progressStatus.textContent = '完成';
        progressStatus.style.background = 'rgba(23, 191, 99, 0.1)';
        progressStatus.style.color = '#17bf63';
    }
}

// ========== 重置表单 ==========
function resetForm() {
    document.getElementById('scraperForm').style.display = 'block';
    document.getElementById('progressContainer').style.display = 'none';
    document.getElementById('actionButtons').style.display = 'none';
    
    // 重置进度
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('progressText').textContent = '0%';
    document.getElementById('currentTweets').textContent = '0';
    document.getElementById('targetTweets').textContent = '0';
    
    currentFiles = [];
    
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
        statusCheckInterval = null;
    }
}

// ========== 预览数据 ==========
async function previewData() {
    if (currentFiles.length === 0) {
        showNotification('没有可预览的文件', 'error');
        return;
    }
    
    // 优先查找CSV文件，其次JSON文件
    let fileToPreview = currentFiles.find(f => f.type === 'csv');
    if (!fileToPreview) {
        fileToPreview = currentFiles.find(f => f.type === 'json');
    }
    
    if (!fileToPreview) {
        showNotification('没有可预览的文件', 'error');
        return;
    }
    
    try {
        const response = await fetch(`/api/preview/${fileToPreview.name}`);
        const data = await response.json();
        
        if (response.ok) {
            displayPreview(data, fileToPreview.name);
        } else {
            showNotification(data.error || '预览失败', 'error');
        }
    } catch (error) {
        showNotification('预览失败: ' + error.message, 'error');
    }
}

// ========== 显示预览 ==========
function displayPreview(data, filename) {
    const modal = document.getElementById('previewModal');
    const previewContent = document.getElementById('previewContent');
    
    // 判断文件格式
    const format = data.format || (filename && filename.endsWith('.csv') ? 'csv' : 'json');
    const formatLabel = format.toUpperCase();
    
    let html = `<div style="margin-bottom: 20px; color: var(--text-secondary);">
        <span style="background: var(--primary); color: white; padding: 4px 12px; border-radius: 6px; margin-right: 10px;">${formatLabel}</span>
        显示前10条，共${data.total}条推文
    </div>`;
    
    data.tweets.forEach((tweet, index) => {
        html += `
            <div class="tweet-preview">
                <div class="tweet-text">${escapeHtml(tweet.text)}</div>
                <div class="tweet-meta">
                    <div class="tweet-stats">
                        <i class="fas fa-heart"></i>
                        <span>${tweet.likes || 0}</span>
                    </div>
                    <div class="tweet-stats">
                        <i class="fas fa-retweet"></i>
                        <span>${tweet.retweets || 0}</span>
                    </div>
                    <div class="tweet-stats">
                        <i class="fas fa-comment"></i>
                        <span>${tweet.replies || 0}</span>
                    </div>
                    <div class="tweet-stats">
                        <i class="fas fa-clock"></i>
                        <span>${tweet.time_display || '未知'}</span>
                    </div>
                </div>
            </div>
        `;
    });
    
    previewContent.innerHTML = html;
    modal.classList.add('show');
}

// ========== 关闭模态框 ==========
function closeModal() {
    const modal = document.getElementById('previewModal');
    modal.classList.remove('show');
}

// 点击模态框外部关闭
document.addEventListener('click', function(e) {
    const modal = document.getElementById('previewModal');
    if (e.target === modal) {
        closeModal();
    }
});

// ========== 下载文件 ==========
function downloadFiles() {
    if (currentFiles.length === 0) {
        showNotification('没有可下载的文件', 'error');
        return;
    }
    
    currentFiles.forEach(file => {
        const link = document.createElement('a');
        link.href = `/api/download/${file.name}`;
        link.download = file.name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
    
    showNotification(`正在下载 ${currentFiles.length} 个文件`, 'success');
}

// ========== 加载历史记录 ==========
async function loadHistory() {
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = `
        <div class="loading-spinner">
            <i class="fas fa-spinner fa-spin"></i>
            <p>加载中...</p>
        </div>
    `;
    
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        if (data.files && data.files.length > 0) {
            displayHistory(data.files);
        } else {
            historyList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-folder-open"></i>
                    <p>暂无历史记录</p>
                </div>
            `;
        }
    } catch (error) {
        historyList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <p>加载失败: ${error.message}</p>
            </div>
        `;
    }
}

// ========== 显示历史记录 ==========
function displayHistory(files) {
    const historyList = document.getElementById('historyList');
    
    let html = '';
    files.forEach(file => {
        const fileSize = formatFileSize(file.size);
        const fileDate = formatDate(file.modified);
        const fileIcon = file.type === 'JSON' ? 'fa-file-code' : 'fa-file-csv';
        
        html += `
            <div class="history-item">
                <div class="history-info">
                    <div class="file-icon">
                        <i class="fas ${fileIcon}"></i>
                    </div>
                    <div class="file-details">
                        <h4>${file.name}</h4>
                        <div class="file-meta">
                            <span><i class="fas fa-tag"></i> ${file.type}</span>
                            <span><i class="fas fa-hdd"></i> ${fileSize}</span>
                            <span><i class="fas fa-calendar"></i> ${fileDate}</span>
                        </div>
                    </div>
                </div>
                <div class="history-actions">
                    <button class="icon-btn" onclick="previewHistoryFile('${file.name}')" title="预览">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="icon-btn" onclick="downloadHistoryFile('${file.name}')" title="下载">
                        <i class="fas fa-download"></i>
                    </button>
                </div>
            </div>
        `;
    });
    
    historyList.innerHTML = html;
}

// ========== 预览历史文件 ==========
async function previewHistoryFile(filename) {
    try {
        const response = await fetch(`/api/preview/${filename}`);
        const data = await response.json();
        
        if (response.ok) {
            displayPreview(data, filename);
        } else {
            showNotification(data.error || '预览失败', 'error');
        }
    } catch (error) {
        showNotification('预览失败: ' + error.message, 'error');
    }
}

// ========== 下载历史文件 ==========
function downloadHistoryFile(filename) {
    const link = document.createElement('a');
    link.href = `/api/download/${filename}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showNotification('开始下载', 'success');
}

// ========== 工具函数 ==========
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const diff = now - date;
    const hours = Math.floor(diff / 3600000);
    
    if (hours < 1) {
        return '刚刚';
    } else if (hours < 24) {
        return `${hours}小时前`;
    } else if (hours < 48) {
        return '昨天';
    } else {
        return date.toLocaleDateString('zh-CN');
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#17bf63' : type === 'error' ? '#f91880' : '#1DA1F2'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        z-index: 3000;
        animation: slideInRight 0.3s ease;
        font-weight: 600;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // 3秒后移除
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// 添加通知动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

