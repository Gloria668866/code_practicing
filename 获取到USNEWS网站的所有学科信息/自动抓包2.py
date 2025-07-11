#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能US News爬虫 - 处理多种数据加载方式
"""

import time
import json
import requests
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SmartUSNewsScraper:
    def __init__(self, headless=False):
        self.url = "https://www.usnews.com/best-graduate-schools/top-business-schools/executive-rankings"
        self.headless = headless
        self.driver = None
        self.data = []

    def setup_driver(self):
        """设置Chrome浏览器"""
        options = Options()

        if self.headless:
            options.add_argument('--headless')

        # 启用网络日志
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        # 反检测配置
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # 设置用户代理
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.add_argument('--window-size=1920,1080')

        try:
            service = Service(
                executable_path=r'C:\Users\Administrator\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')
            self.driver = webdriver.Chrome(service=service, options=options)

            # 执行反检测脚本
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            print("浏览器设置完成")
            return self.driver

        except Exception as e:
            print(f"浏览器设置失败: {e}")
            raise

    def get_network_requests(self):
        """获取网络请求"""
        logs = self.driver.get_log('performance')
        requests = []

        for log in logs:
            try:
                message = json.loads(log['message'])
                if 'message' in message:
                    if message['message']['method'] == 'Network.requestWillBeSent':
                        request = message['message']['params']
                        requests.append({
                            'url': request['request']['url'],
                            'method': request['request']['method'],
                            'type': request.get('type', 'unknown')
                        })
            except:
                continue

        return requests

    def find_api_endpoints(self):
        """查找API端点"""
        print("查找API端点...")

        requests = self.get_network_requests()
        api_endpoints = []

        # 过滤可能的API请求
        keywords = ['api', 'data', 'rankings', 'schools', 'business', 'executive', 'json']

        for req in requests:
            url = req['url'].lower()
            if any(keyword in url for keyword in keywords):
                api_endpoints.append(req)

        print(f"找到 {len(api_endpoints)} 个可能的API端点")
        return api_endpoints

    def try_direct_api_access(self, api_url):
        """尝试直接访问API"""
        print(f"尝试直接访问API: {api_url}")

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': self.url
            }

            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code == 200:
                try:
                    data = response.json()
                    return data
                except:
                    print("响应不是有效的JSON格式")
                    return None
            else:
                print(f"API请求失败，状态码: {response.status_code}")
                return None

        except Exception as e:
            print(f"访问API失败: {e}")
            return None

    def extract_data_from_page_source(self):
        """从页面源码中提取数据"""
        print("从页面源码中提取数据...")

        page_source = self.driver.page_source

        # 查找可能的JSON数据
        patterns = [
            r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
            r'window\.data\s*=\s*({.*?});',
            r'var\s+data\s*=\s*({.*?});',
            r'"schools":\s*\[(.*?)\]',
            r'"rankings":\s*\[(.*?)\]',
            r'"universities":\s*\[(.*?)\]',
            r'"institutions":\s*\[(.*?)\]'
        ]

        found_data = []

        for pattern in patterns:
            matches = re.findall(pattern, page_source, re.DOTALL)
            if matches:
                print(f"找到匹配模式: {pattern}")
                found_data.extend(matches)

        return found_data

    def extract_data_with_js(self):
        """使用JavaScript提取数据"""
        print("使用JavaScript提取数据...")

        # 等待页面加载
        time.sleep(5)

        # 滚动页面触发懒加载
        for i in range(3):
            self.driver.execute_script(f"window.scrollTo(0, {1000 * (i + 1)});")
            time.sleep(2)

        # 使用JavaScript提取数据
        js_scripts = [
            # 策略1: 查找所有文本内容
            """
            return Array.from(document.querySelectorAll('*')).filter(el => {
                const text = el.textContent || '';
                return text.length > 10 && text.length < 500 &&
                       (text.includes('University') || text.includes('College') || 
                        text.includes('School') || text.includes('Institute'));
            }).map(el => ({
                text: el.textContent.trim(),
                tagName: el.tagName,
                className: el.className,
                id: el.id
            }));
            """,

            # 策略2: 查找数字排名
            """
            return Array.from(document.querySelectorAll('*')).filter(el => {
                const text = el.textContent || '';
                return /^\\d+$/.test(text.trim()) && 
                       text.trim().length <= 3 && 
                       parseInt(text.trim()) <= 100;
            }).map(el => ({
                rank: el.textContent.trim(),
                tagName: el.tagName,
                className: el.className,
                parentText: el.parentElement ? el.parentElement.textContent.trim() : ''
            }));
            """,

            # 策略3: 查找评分
            """
            return Array.from(document.querySelectorAll('*')).filter(el => {
                const text = el.textContent || '';
                return /\\d+\\.\\d+/.test(text) && 
                       text.includes('.') && 
                       parseFloat(text) <= 100;
            }).map(el => ({
                score: el.textContent.trim(),
                tagName: el.tagName,
                className: el.className,
                parentText: el.parentElement ? el.parentElement.textContent.trim() : ''
            }));
            """
        ]

        results = {}

        for i, script in enumerate(js_scripts):
            try:
                result = self.driver.execute_script(script)
                results[f'strategy_{i + 1}'] = result
                print(f"策略{i + 1}提取到 {len(result)} 条数据")
            except Exception as e:
                print(f"策略{i + 1}执行失败: {e}")

        return results

    def process_extracted_data(self, js_data, api_data=None, page_data=None):
        """处理提取到的数据"""
        print("处理提取到的数据...")

        schools = []

        # 处理JavaScript提取的数据
        if js_data:
            # 处理学校名称
            for item in js_data.get('strategy_1', []):
                text = item.get('text', '')
                if self.is_valid_school_name(text):
                    schools.append({
                        'name': text,
                        'rank': 'N/A',
                        'score': 'N/A',
                        'location': 'N/A',
                        'source': 'javascript'
                    })

            # 处理排名
            for rank_item in js_data.get('strategy_2', []):
                rank = rank_item.get('rank', '')
                parent_text = rank_item.get('parentText', '')

                for school in schools:
                    if school['name'] in parent_text:
                        school['rank'] = rank
                        break

            # 处理评分
            for score_item in js_data.get('strategy_3', []):
                score = score_item.get('score', '')
                parent_text = score_item.get('parentText', '')

                for school in schools:
                    if school['name'] in parent_text:
                        school['score'] = score
                        break

        # 处理API数据
        if api_data:
            print("处理API数据...")
            # 这里需要根据实际的API数据结构来解析
            # 暂时跳过，等找到正确的API后再实现

        # 处理页面源码数据
        if page_data:
            print("处理页面源码数据...")
            # 这里需要根据实际的页面数据结构来解析
            # 暂时跳过，等找到正确的数据结构后再实现

        return schools

    def is_valid_school_name(self, text):
        """判断是否为有效的学校名称"""
        if not text or len(text) < 5 or len(text) > 100:
            return False

        # 包含学校关键词
        school_keywords = ['university', 'college', 'school', 'institute', 'academy']
        text_lower = text.lower()

        return any(keyword in text_lower for keyword in school_keywords)

    def save_data(self, schools, filename=None):
        """保存数据"""
        if not filename:
            filename = f"usnews_schools_smart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # 添加时间戳
        for school in schools:
            school['timestamp'] = datetime.now().isoformat()

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(schools, f, ensure_ascii=False, indent=2)

        print(f"数据已保存到: {filename}")
        print(f"共提取 {len(schools)} 所学校的数据")

        # 打印结果
        for school in schools:
            print(f"- {school['name']}: 排名{school['rank']}, 评分{school['score']}, 位置{school['location']}")

    def run(self):
        """运行爬虫"""
        try:
            print("开始智能抓取US News商学院排名...")

            # 设置浏览器
            self.setup_driver()

            # 访问页面
            print(f"正在访问: {self.url}")
            self.driver.get(self.url)

            # 等待页面加载
            time.sleep(10)

            # 方法1: 查找API端点
            api_endpoints = self.find_api_endpoints()

            api_data = None
            if api_endpoints:
                print("尝试访问API端点...")
                for endpoint in api_endpoints[:3]:  # 只尝试前3个
                    api_data = self.try_direct_api_access(endpoint['url'])
                    if api_data:
                        print(f"成功从API获取数据: {endpoint['url']}")
                        break

            # 方法2: 从页面源码提取数据
            page_data = self.extract_data_from_page_source()

            # 方法3: 使用JavaScript提取数据
            js_data = self.extract_data_with_js()

            # 处理所有提取到的数据
            schools = self.process_extracted_data(js_data, api_data, page_data)

            # 保存数据
            self.save_data(schools)

            # 保存分析结果
            analysis_result = {
                'timestamp': datetime.now().isoformat(),
                'url': self.url,
                'api_endpoints_found': len(api_endpoints),
                'page_data_snippets': len(page_data),
                'js_data_strategies': len(js_data),
                'schools_extracted': len(schools)
            }

            with open('smart_analysis.json', 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=2)

            print(f"分析结果已保存到: smart_analysis.json")

        except Exception as e:
            print(f"爬虫运行出错: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.driver:
                self.driver.quit()
                print("浏览器已关闭")


def main():
    """主函数"""
    print("=" * 60)
    print("智能US News爬虫")
    print("=" * 60)
    print("功能：")
    print("1. 查找API端点")
    print("2. 从页面源码提取数据")
    print("3. 使用JavaScript提取数据")
    print("4. 多种策略结合")
    print("=" * 60)

    scraper = SmartUSNewsScraper(headless=False)
    scraper.run()


if __name__ == "__main__":
    main()
