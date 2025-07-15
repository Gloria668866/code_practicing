import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from datetime import datetime

API_URL = "http://10.9.8.118:5001/api/req_data/get_gzh"

ALERT_SECONDS = 68 * 3600  # 68小时
VALID_SECONDS = 72 * 3600  # 72小时

def get_json_by_selenium(url):
    """
    用Selenium无头模式访问接口并返回json数据
    """
    options = Options()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(3)
        text = driver.page_source
        if text.strip().startswith("<html"):
            soup = BeautifulSoup(text, "html.parser")
            text = soup.get_text()
        text = text.strip()
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"Selenium获取json失败: {e}")
        return None
    finally:
        driver.quit()

FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/0e49fa1d-c122-454f-9798-7c1d5753675d"

def send_feishu_msg(content):
    headers = {"Content-Type": "application/json"}
    data = {
        "msg_type": "text",
        "content": {
            "text": content
        }
    }
    resp = requests.post(FEISHU_WEBHOOK, json=data, headers=headers)
    print("飞书推送返回：", resp.text)
    print("[飞书推送已注释]", content)

def main():
    data = get_json_by_selenium(API_URL)
    if not data:
        print("未获取到数据，退出")
        return
    now = int(time.time())
    for item in data.get("data", []):
        nickname = item.get("Nickname", "")
        updated_at = int(item.get("UpdatedAt", 0))
        expire_ts = updated_at + VALID_SECONDS
        left_sec = expire_ts - now
        left_hour = left_sec // 3600
        left_min = (left_sec % 3600) // 60
        expire_time = datetime.fromtimestamp(expire_ts).strftime("%Y-%m-%d %H:%M:%S")
        if now > updated_at + ALERT_SECONDS:
            msg = f"【预警】公众号【{nickname}】参数将于 {expire_time} 过期，剩余{left_hour}小时{left_min}分钟，请及时处理！"
            print(msg)
            send_feishu_msg(msg)  # 飞书推送已注释
        else:
            print(f"公众号【{nickname}】参数安全，剩余{left_hour}小时{left_min}分钟，有效期至{expire_time}")

if __name__ == '__main__':
    main()
