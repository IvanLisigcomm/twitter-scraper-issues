#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X（推特）推文爬虫程序
模拟人工浏览行为，获取指定用户的推文内容
"""

import os
import json
import csv
import time
import random
import shutil
from datetime import datetime
from typing import List, Dict, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class TwitterScraper:
    """X（推特）推文爬虫类"""
    
    def __init__(self, headless: bool = False, delay_range: tuple = (2, 5), progress_callback=None, control_callback=None):
        """
        初始化爬虫
        
        Args:
            headless: 是否使用无头模式
            delay_range: 随机延迟范围（秒）
            progress_callback: 进度回调函数，接受 (current, total, message) 参数
            control_callback: 控制回调函数，返回 (is_paused, is_cancelled) 元组
        """
        self.headless = headless
        self.delay_range = delay_range
        self.driver = None
        self.tweets_data = []
        self.username = None  # 保存当前爬取的用户名
        self.progress_callback = progress_callback  # 保存进度回调函数
        self.control_callback = control_callback  # 保存控制回调函数
        
        # 创建 data 目录
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"已创建数据目录: {self.data_dir}")
        
    def setup_driver(self) -> webdriver.Chrome:
        """设置Chrome浏览器驱动"""
        print("正在设置浏览器驱动...")
        
        # Chrome选项配置
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
            
        # 反检测配置
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 设置随机User-Agent
        ua = UserAgent()
        chrome_options.add_argument(f'--user-agent={ua.random}')
        
        # 窗口大小
        chrome_options.add_argument('--window-size=1920,1080')
        
        # 创建驱动 - 添加重试机制和更好的错误处理
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"尝试安装 ChromeDriver (第 {attempt + 1} 次)...")
                
                # 使用 webdriver-manager 安装 ChromeDriver
                driver_path = ChromeDriverManager().install()
                print(f"webdriver-manager 返回路径: {driver_path}")
                
                # 修复路径问题 - 查找实际的 chromedriver 可执行文件
                if 'THIRD_PARTY_NOTICES' in driver_path or not driver_path.endswith('chromedriver'):
                    # 在同一目录下查找真正的 chromedriver 文件
                    driver_dir = os.path.dirname(driver_path)
                    possible_paths = [
                        os.path.join(driver_dir, 'chromedriver'),
                        os.path.join(driver_dir, 'chromedriver-mac-arm64'),
                        os.path.join(driver_dir, 'chromedriver-mac-x64')
                    ]
                    
                    actual_driver_path = None
                    for path in possible_paths:
                        if os.path.exists(path):
                            # 先设置执行权限，然后检查
                            os.chmod(path, 0o755)
                            if os.access(path, os.X_OK):
                                actual_driver_path = path
                                break
                    
                    if actual_driver_path:
                        driver_path = actual_driver_path
                        print(f"找到实际的 ChromeDriver: {driver_path}")
                    else:
                        # 列出目录内容以调试
                        print(f"目录内容: {os.listdir(driver_dir)}")
                        raise FileNotFoundError(f"在 {driver_dir} 中找不到可执行的 chromedriver")
                
                # 检查文件是否存在且可执行
                if not os.path.exists(driver_path):
                    raise FileNotFoundError(f"ChromeDriver 文件不存在: {driver_path}")
                
                # 在 macOS 上设置执行权限
                if os.name != 'nt':  # 非 Windows 系统
                    os.chmod(driver_path, 0o755)
                    print(f"已设置 ChromeDriver 执行权限")
                
                service = Service(driver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # 执行反检测脚本
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                self.driver = driver
                print("浏览器驱动设置成功！")
                return driver
                
            except Exception as e:
                print(f"第 {attempt + 1} 次尝试失败: {e}")
                if attempt < max_retries - 1:
                    print("正在重试...")
                    # 清理可能损坏的缓存
                    import shutil
                    wdm_cache = os.path.expanduser("~/.wdm")
                    if os.path.exists(wdm_cache):
                        shutil.rmtree(wdm_cache)
                        print("已清理 webdriver-manager 缓存")
                    time.sleep(2)
                else:
                    print("所有尝试都失败了，请检查 Chrome 浏览器是否已安装")
                    raise e
    
    def random_delay(self, min_delay: Optional[float] = None, max_delay: Optional[float] = None):
        """随机延迟"""
        if min_delay is None:
            min_delay = self.delay_range[0]
        if max_delay is None:
            max_delay = self.delay_range[1]
            
        delay = random.uniform(min_delay, max_delay)
        print(f"等待 {delay:.2f} 秒...")
        time.sleep(delay)
    
    def scroll_page(self, scrolls: int = 3):
        """模拟滚动页面加载更多内容"""
        print(f"正在滚动页面加载更多内容...")
        
        for i in range(scrolls):
            # 获取当前页面高度
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # 尝试滚动到最后一个推文元素的位置
            try:
                last_tweet = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')[-1]
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", last_tweet)
                print(f"  滚动 {i+1}/{scrolls}: 滚动到最后一个推文...")
            except:
                # 如果失败，就滚动到页面底部
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print(f"  滚动 {i+1}/{scrolls}: 滚动到底部...")
            
            # 等待新内容加载
            self.random_delay(2, 4)
            
            # 检查页面高度是否改变（说明加载了新内容）
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height > last_height:
                print(f"  ✓ 页面高度增加: {last_height} -> {new_height}")
            else:
                print(f"  ⚠ 页面高度未变化，可能已到底部")
            
            # 稍微往回滚一点，模拟真实浏览行为
            if i < scrolls - 1:  # 最后一次不往回滚
                self.driver.execute_script("window.scrollBy(0, -300);")
                self.random_delay(0.5, 1)
    
    def extract_tweet_data(self, tweet_element) -> Optional[Dict]:
        """从推文元素中提取数据"""
        try:
            tweet_data = {}
            
            # 获取推文HTML
            tweet_html = tweet_element.get_attribute('innerHTML')
            soup = BeautifulSoup(tweet_html, 'html.parser')
            
            # 提取推文文本
            text_elements = tweet_element.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')
            if text_elements:
                tweet_data['text'] = text_elements[0].text
            else:
                tweet_data['text'] = ""
            
            # 提取时间
            try:
                time_element = tweet_element.find_element(By.CSS_SELECTOR, 'time')
                tweet_data['timestamp'] = time_element.get_attribute('datetime')
                tweet_data['time_display'] = time_element.text
            except NoSuchElementException:
                tweet_data['timestamp'] = ""
                tweet_data['time_display'] = ""
            
            # 提取互动数据（点赞、转发、评论）
            try:
                # 点赞数
                like_elements = tweet_element.find_elements(By.CSS_SELECTOR, '[data-testid="like"]')
                if like_elements:
                    like_text = like_elements[0].get_attribute('aria-label') or "0"
                    tweet_data['likes'] = self.extract_number_from_text(like_text)
                else:
                    tweet_data['likes'] = 0
                
                # 转发数
                retweet_elements = tweet_element.find_elements(By.CSS_SELECTOR, '[data-testid="retweet"]')
                if retweet_elements:
                    retweet_text = retweet_elements[0].get_attribute('aria-label') or "0"
                    tweet_data['retweets'] = self.extract_number_from_text(retweet_text)
                else:
                    tweet_data['retweets'] = 0
                
                # 评论数
                reply_elements = tweet_element.find_elements(By.CSS_SELECTOR, '[data-testid="reply"]')
                if reply_elements:
                    reply_text = reply_elements[0].get_attribute('aria-label') or "0"
                    tweet_data['replies'] = self.extract_number_from_text(reply_text)
                else:
                    tweet_data['replies'] = 0
                    
            except Exception as e:
                print(f"提取互动数据时出错: {e}")
                tweet_data['likes'] = 0
                tweet_data['retweets'] = 0
                tweet_data['replies'] = 0
            
            # 添加爬取时间
            tweet_data['scraped_at'] = datetime.now().isoformat()
            
            return tweet_data
            
        except Exception as e:
            print(f"提取推文数据时出错: {e}")
            return None
    
    def extract_number_from_text(self, text: str) -> int:
        """从文本中提取数字"""
        try:
            # 处理包含K、M等单位的数字
            text = text.lower().replace(',', '')
            if 'k' in text:
                number = float(text.replace('k', '')) * 1000
            elif 'm' in text:
                number = float(text.replace('m', '')) * 1000000
            else:
                # 提取纯数字
                import re
                numbers = re.findall(r'\d+', text)
                number = int(numbers[0]) if numbers else 0
            return int(number)
        except:
            return 0
    
    def scrape_user_tweets(self, username: str, max_tweets: int = 50) -> List[Dict]:
        """
        爬取指定用户的推文
        
        Args:
            username: 用户名（不包含@符号）
            max_tweets: 最大爬取推文数量
            
        Returns:
            推文数据列表
        """
        if not self.driver:
            self.setup_driver()
        
        # 保存用户名，用于后续文件命名
        self.username = username
        
        print(f"开始爬取用户 @{username} 的推文...")
        
        # 访问用户主页
        url = f"https://x.com/{username}"
        print(f"正在访问: {url}")
        
        try:
            self.driver.get(url)
            self.random_delay(3, 6)
            
            # 等待页面加载
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]'))
            )
            
            # 初始化进度
            if self.progress_callback:
                self.progress_callback(0, max_tweets, "页面加载完成，开始爬取推文...")
            
            tweets_collected = 0
            scroll_attempts = 0
            max_scroll_attempts = 20  # 增加滚动次数
            no_new_tweets_count = 0  # 连续没有新推文的次数
            
            # 用于去重的集合（使用timestamp+text的组合）
            seen_tweets = set()
            
            while tweets_collected < max_tweets and scroll_attempts < max_scroll_attempts:
                # 检查控制标志（暂停/取消）
                if self.control_callback:
                    is_paused, is_cancelled = self.control_callback()
                    
                    # 如果被取消，立即退出
                    if is_cancelled:
                        print("\n❌ 爬取任务已被取消")
                        break
                    
                    # 如果被暂停，等待恢复
                    while is_paused:
                        print("⏸️  任务已暂停，等待恢复...")
                        time.sleep(1)
                        is_paused, is_cancelled = self.control_callback()
                        if is_cancelled:
                            print("\n❌ 爬取任务已被取消")
                            break
                    
                    # 如果在暂停期间被取消，退出
                    if is_cancelled:
                        break
                
                print(f"\n=== 第 {scroll_attempts + 1} 轮爬取 ===")
                print(f"已收集 {tweets_collected}/{max_tweets} 条推文")
                
                # 查找推文元素
                tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
                print(f"当前页面共找到 {len(tweet_elements)} 个推文元素")
                
                # 提取新推文 - 遍历所有元素，使用去重集合来避免重复
                new_tweets_in_this_scroll = 0
                for tweet_element in tweet_elements:
                    if tweets_collected >= max_tweets:
                        break
                        
                    tweet_data = self.extract_tweet_data(tweet_element)
                    if tweet_data and tweet_data['text'].strip():
                        # 使用 timestamp + text 作为唯一标识
                        tweet_id = f"{tweet_data.get('timestamp', '')}_{tweet_data['text']}"
                        
                        # 检查是否已经收集过这条推文
                        if tweet_id not in seen_tweets:
                            seen_tweets.add(tweet_id)
                            self.tweets_data.append(tweet_data)
                            tweets_collected += 1
                            new_tweets_in_this_scroll += 1
                            print(f"  ✓ 新推文 #{tweets_collected}: {tweet_data['text'][:50]}...")
                            
                            # 更新进度
                            if self.progress_callback:
                                self.progress_callback(tweets_collected, max_tweets, f"正在爬取推文...已收集 {tweets_collected}/{max_tweets} 条")
                
                print(f"→ 本轮收集到 {new_tweets_in_this_scroll} 条新推文")
                
                # 如果已达到目标数量，退出
                if tweets_collected >= max_tweets:
                    print(f"\n✅ 已达到目标数量 {max_tweets} 条！")
                    break
                
                # 如果连续多次滚动都没有新推文，可能已经到底了
                if new_tweets_in_this_scroll == 0:
                    no_new_tweets_count += 1
                    print(f"⚠️  本轮无新推文（连续 {no_new_tweets_count} 次）")
                    if no_new_tweets_count >= 3:
                        print("❌ 连续3次滚动都没有新推文，可能已经到达页面底部")
                        break
                else:
                    no_new_tweets_count = 0  # 重置计数器
                
                # 滚动加载更多
                print("\n📜 开始滚动加载更多推文...")
                if self.progress_callback:
                    self.progress_callback(tweets_collected, max_tweets, f"正在滚动页面加载更多推文...已收集 {tweets_collected}/{max_tweets} 条")
                
                prev_elements_count = len(tweet_elements)
                self.scroll_page(3)
                scroll_attempts += 1
                
                # 滚动后等待新内容加载
                print("⏳ 等待新推文加载...")
                self.random_delay(3, 5)
                
                # 检查是否真的加载了新元素
                new_tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
                if len(new_tweet_elements) > prev_elements_count:
                    print(f"✓ 页面元素增加: {prev_elements_count} -> {len(new_tweet_elements)}")
                else:
                    print(f"⚠️  页面元素未增加，仍为 {len(new_tweet_elements)} 个")
            
            # 按时间戳排序（从新到旧）
            print("\n正在按时间排序推文...")
            self.tweets_data.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            print(f"爬取完成！共收集到 {len(self.tweets_data)} 条推文")
            return self.tweets_data
            
        except TimeoutException:
            print("页面加载超时，可能用户不存在或网络问题")
            return []
        except Exception as e:
            print(f"爬取过程中出现错误: {e}")
            return []
    
    def save_to_json(self, filename: str = None):
        """保存数据为JSON格式"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # 使用用户名+时间戳命名
            username_part = self.username if self.username else "tweets"
            filename = f"{username_part}_{timestamp}.json"
        
        # 保存到 data 目录
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.tweets_data, f, ensure_ascii=False, indent=2)
        
        print(f"数据已保存到: {filepath}")
        return filepath
    
    def save_to_csv(self, filename: str = None):
        """保存数据为CSV格式"""
        if not self.tweets_data:
            print("没有数据可保存")
            return None
            
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # 使用用户名+时间戳命名
            username_part = self.username if self.username else "tweets"
            filename = f"{username_part}_{timestamp}.csv"
        
        # 保存到 data 目录
        filepath = os.path.join(self.data_dir, filename)
        
        fieldnames = ['text', 'timestamp', 'time_display', 'likes', 'retweets', 'replies', 'scraped_at']
        
        # 使用 utf-8-sig 编码，添加 BOM 标记，让 Excel 能正确识别 UTF-8 编码
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for tweet in self.tweets_data:
                writer.writerow(tweet)
        
        print(f"数据已保存到: {filepath}")
        print("提示: CSV 文件使用 UTF-8 BOM 编码，可在 Excel 中正常显示中文")
        return filepath
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("浏览器已关闭")


def main():
    """主函数"""
    print("=== X（推特）推文爬虫程序 ===")
    print()
    
    # 获取用户输入
    username = input("请输入要爬取的用户名（不包含@符号）: ").strip()
    if not username:
        print("用户名不能为空！")
        return
    
    try:
        max_tweets = int(input("请输入要爬取的推文数量（默认50）: ") or "50")
    except ValueError:
        max_tweets = 50
    
    headless_input = input("是否使用无头模式？(y/N): ").strip().lower()
    headless = headless_input in ['y', 'yes', '是']
    
    save_format = input("选择保存格式 (json/csv/both，默认csv): ").strip().lower() or "csv"
    
    print()
    print("开始爬取...")
    
    # 创建爬虫实例
    scraper = TwitterScraper(headless=headless)
    
    try:
        # 爬取推文
        tweets = scraper.scrape_user_tweets(username, max_tweets)
        
        if tweets:
            print(f"\n成功爬取到 {len(tweets)} 条推文！")
            
            # 保存数据
            if save_format in ['json', 'both']:
                scraper.save_to_json()
            
            if save_format in ['csv', 'both']:
                scraper.save_to_csv()
            
            print("\n爬取任务完成！")
        else:
            print("没有爬取到任何推文，请检查用户名是否正确或网络连接")
    
    except KeyboardInterrupt:
        print("\n用户中断了程序")
    except Exception as e:
        print(f"\n程序执行出错: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
