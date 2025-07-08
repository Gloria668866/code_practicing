from concurrent.futures import ThreadPoolExecutor, as_completed
import pymysql
import requests
from webcontent import WebContent
import platform
from bs4 import BeautifulSoup
from DrissionPage import ChromiumPage, ChromiumOptions, WebPage
import time
import json
import re

# Dify API配置
DIFY_API_URL = "http://10.9.8.120:9988/v1/workflows/run"
DIFY_API_KEY = "app-mXpyuHNkqoiXhiKdIZFFVMYy"
WORKFLOW_ID = "34ff25ee-5de7-4d3f-8642-ce2df7b6ce88"
APP_ID = "34ff25ee-5de7-4d3f-8642-ce2df7b6ce88"
USER_ID = "test_user"  # 可自定义
headers = {
    "Authorization": f"Bearer {DIFY_API_KEY}",
    "Content-Type": "application/json",
}

def call_dify_api(url, retry=3):
    data = {
        "workflow_id": WORKFLOW_ID,
        "inputs": {"url": url},
        "user": USER_ID,
        "app_id": APP_ID,
        "response_mode": "blocking",
    }
    for i in range(retry):
        try:
            response = requests.post(DIFY_API_URL, headers=headers, json=data, timeout=180)
            if response.status_code == 429:
                print("被限流，等待5秒重试...")
                time.sleep(5)
                continue
            if response.status_code == 200:
                result = response.json()
                print("✅ Dify返回：", result)
                return result
            else:
                print(f"❌ Dify请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Dify请求异常: {e}")
            time.sleep(5)
    return None

def get_urls():
    conn = pymysql.connect(
        host='10.9.8.120',
        user='lgb_dbs',
        port=3306,
        password='lgb123456',
        database='bestieu_test2',
        charset='utf8mb4'
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT biz FROM wechat_official_account_info WHERE bu_type=1")
            biz_list = [row[0] for row in cursor.fetchall()]
            urls = []
            for biz in biz_list:
                cursor.execute("SELECT url FROM wechat_official_account_articles WHERE wx_id=%s", (biz,))
                urls += [row[0] for row in cursor.fetchall()]
            return urls
    finally:
        conn.close()

def write_sql_to_db(sql):
    if not sql or not sql.strip().lower().startswith("insert"):
        print(f"⚠ AI返回的SQL不合法，跳过。内容：{sql}")
        return
    try:
        conn = pymysql.connect(
            host='10.9.8.120',
            user='lgb_dbs',
            port=3306,
            password='lgb123456',
            database='bestieu_test2',
            charset='utf8mb4'
        )
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
        print("✅ SQL写入数据库成功！")
    except Exception as e:
        print(f"❌ SQL写入数据库失败: {e}\nSQL: {sql}")
    finally:
        conn.close()

def extract_sql(ai_text):
    ai_text = ai_text.strip().strip('"').strip("'")
    ai_text = ai_text.replace('\n', '').replace('\r', '')
    if ai_text.lower().startswith("insert into"):
        return ai_text
    match = re.search(r"(INSERT INTO[\s\S]+?;)", ai_text, re.IGNORECASE)
    if match:
        sql = match.group(1)
        sql = sql.replace('\n', '').replace('\r', '').replace('```', '').strip()
        return sql
    return None

def process_url(url):
    web_content = WebContent()
    html = web_content.get_html_via_drission(url)
    if not html or len(html) < 100:
        print(f"网页内容获取失败，跳过：{url}")
        return
    result = call_dify_api(url)
    if result:
        ai_text = ""
        try:
            ai_text = result['data']['outputs']['result']
        except Exception as e:
            print("无法从Dify结果中提取SQL，原始返回：", result)
        sql = extract_sql(ai_text)
        if sql:
            write_sql_to_db(sql)
            print("提取到SQL：", sql)
        else:
            print("AI原始返回内容：", repr(ai_text))
            print("未能提取到有效SQL")
    time.sleep(5)  # 节流，防止请求过快
def main():
    urls = get_urls()
    print(f"共获取到 {len(urls)} 个URL，开始并发处理...")

    max_workers = 3  # 线程数可根据实际情况调整，建议从5开始，逐步测试
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_url, url) for url in urls]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print("处理某个URL时出错：", e)

if __name__ == "__main__":
    main()
