#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络请求分析器 - 找到US News的数据接口
"""

import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver_with_network_logging():
    """设置Chrome浏览器并启用网络日志"""
    options = Options()

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
        driver = webdriver.Chrome(service=service, options=options)

        # 执行反检测脚本
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print("浏览器设置完成，已启用网络日志")
        return driver

    except Exception as e:
        print(f"浏览器设置失败: {e}")
        raise


def get_network_requests(driver):
    """获取网络请求日志"""
    logs = driver.get_log('performance')
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
                        'type': request.get('type', 'unknown'),
                        'timestamp': message['message']['params'].get('timestamp', 0)
                    })
        except:
            continue

    return requests


def analyze_api_endpoints(requests):
    """分析API端点"""
    print("分析网络请求...")

    # 过滤可能的API请求
    api_requests = []
    keywords = ['api', 'data', 'rankings', 'schools', 'business', 'executive', 'json']

    for req in requests:
        url = req['url'].lower()
        if any(keyword in url for keyword in keywords):
            api_requests.append(req)

    print(f"找到 {len(api_requests)} 个可能的API请求:")

    for i, req in enumerate(api_requests[:10]):  # 只显示前10个
        print(f"{i + 1}. {req['method']} {req['url']}")
        print(f"   类型: {req['type']}")
        print()

    return api_requests


def extract_data_from_api(driver, api_url):
    """从API端点提取数据"""
    print(f"尝试从API提取数据: {api_url}")

    try:
        # 直接访问API
        driver.get(api_url)
        time.sleep(3)

        # 获取页面内容
        page_source = driver.page_source

        # 尝试解析JSON
        try:
            data = json.loads(page_source)
            return data
        except:
            print("不是有效的JSON格式")
            return None

    except Exception as e:
        print(f"访问API失败: {e}")
        return None


def find_data_in_page_source(driver):
    """在页面源码中查找数据"""
    print("在页面源码中查找数据...")

    # 获取页面源码
    page_source = driver.page_source

    # 查找可能的JSON数据
    json_patterns = [
        r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
        r'window\.data\s*=\s*({.*?});',
        r'var\s+data\s*=\s*({.*?});',
        r'"schools":\s*\[(.*?)\]',
        r'"rankings":\s*\[(.*?)\]',
        r'"universities":\s*\[(.*?)\]'
    ]

    found_data = []

    for pattern in json_patterns:
        import re
        matches = re.findall(pattern, page_source, re.DOTALL)
        if matches:
            print(f"找到匹配模式: {pattern}")
            found_data.extend(matches)

    return found_data


def main():
    """主函数"""
    print("=" * 60)
    print("US News 网络请求分析器")
    print("=" * 60)
    print("目标：找到数据接口和数据结构")
    print("=" * 60)

    url = "https://www.usnews.com/best-graduate-schools/top-business-schools/executive-rankings"

    try:
        # 设置浏览器
        driver = setup_driver_with_network_logging()

        # 访问页面
        print(f"正在访问: {url}")
        driver.get(url)

        # 等待页面加载
        time.sleep(10)

        # 滚动页面触发更多请求
        print("滚动页面触发更多请求...")
        for i in range(5):
            driver.execute_script(f"window.scrollTo(0, {1000 * (i + 1)});")
            time.sleep(2)

        # 获取网络请求
        requests = get_network_requests(driver)
        print(f"捕获到 {len(requests)} 个网络请求")

        # 分析API端点
        api_requests = analyze_api_endpoints(requests)

        # 在页面源码中查找数据
        found_data = find_data_in_page_source(driver)

        if found_data:
            print(f"在页面源码中找到 {len(found_data)} 个数据片段")
            for i, data in enumerate(found_data[:3]):  # 只显示前3个
                print(f"数据片段 {i + 1}: {data[:200]}...")

        # 尝试访问可能的API
        if api_requests:
            print("\n尝试访问API端点...")
            for req in api_requests[:3]:  # 只尝试前3个
                data = extract_data_from_api(driver, req['url'])
                if data:
                    print(f"成功从API获取数据: {req['url']}")
                    print(f"数据结构: {type(data)}")
                    if isinstance(data, dict):
                        print(f"数据键: {list(data.keys())}")
                    break

        # 保存分析结果
        analysis_result = {
            'timestamp': datetime.now().isoformat(),
            'url': url,
            'total_requests': len(requests),
            'api_requests': api_requests,
            'found_data_snippets': len(found_data)
        }

        with open('network_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)

        print(f"\n分析结果已保存到: network_analysis.json")

    except Exception as e:
        print(f"分析失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'driver' in locals():
            driver.quit()
            print("浏览器已关闭")


if __name__ == "__main__":
    main()
