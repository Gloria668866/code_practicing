import requests,platform
from bs4 import BeautifulSoup
from DrissionPage import ChromiumPage, ChromiumOptions,WebPage
import time
import pymysql

class WebContent:
    def __init__(self, proxy=None):
        self.proxy = proxy or "http://10.9.8.118:41091"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "ua_id=KsUfIsKOrZOyn5k1AAAAADE3J3IMadcgBjs7pV2a7x8=; wxuin=44165380479639; RK=UY2FLl0b/v; ptcz=f5c8dd092aee6810d998914c7dca39cf01a515be99c4c0eee84620ea8313a534; mm_lang=zh_CN; pac_uid=0_jd2JAz0heSkkb; suid=user_0_jd2JAz0heSkkb; _qimei_uuid42=1941212302910040c0b0a5ea54c0a45285004008c8; _qimei_fingerprint=e696194230eb7792e2c8202e516e0fd7; _qimei_q36=; _qimei_h38=fded425ec0b0a5ea54c0a45202000004b19412; yyb_muid=1438BD9B396762100B3AA85A382463E2; poc_sid=HMb1YWijost_4tcWdL5fqmu1L2-ygLGkstyLW2O5; _clck=3191626223|1|fxa|0; rand_info=CAESIFLwyMlf01dUu0/xwGWbtuehk6GjFQKlAJocCxDnfe3c; slave_bizuin=3191626223; data_bizuin=3191626223; bizuin=3191626223; data_ticket=1E7ePgw2I0VfJK7mk8erlFuLyJAqMJAm9HVoGZmJnKxCTp902hyWCGcR0Ht/0kQk; slave_sid=NkpKcWN6TTRKYmQ0UHhxajVOVjNzdXNEbmhwV1hVSEtyMkw4am93dFAwVTJ3VklzZ0hSc3FScEhWX01MT3NiZ2o0empvazlJUUR3d2pGd29qd0FhSXZWZGNvd0lvNXQ1WDVCVXlGQWZXT3VjS1lxSTB2MHpValpJRGtTcDQ5aDBiYld1V1FLOUszemRVdzZj; slave_user=gh_c192ab7528ba; xid=f2b8dbaab88a4804a771f197fde4ce71; rewardsn=; wxtokenkey=777; mm_lang=zh_CN",  # 请替换为最新cookie
            "Origin": "https://mp.weixin.qq.com",
            "Referer": "https://mp.weixin.qq.com/s/sjPnGq68iMkxcfescBLivA",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Requested-With": "XMLHttpRequest"
        }


    def get_html_via_requests(self, url):
        """尝试使用 requests 获取 HTML"""
        try:
            proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
            response = requests.get(url, headers=self.headers, proxies=proxies, timeout=10, verify=False)

            if response.status_code == 200:
                html_text = response.text
                print(f" 获取成功，页面长度: {len(html_text)}")

                if len(html_text) >= 500:
                    soup = BeautifulSoup(html_text, "html.parser")
                    cleaned_html = soup.text.replace("\n", "")
                    print(f"处理后的 HTML 页面长度: {len(cleaned_html)}")
                    return cleaned_html
                else:
                    print("⚠️ requests 获取的内容太短，尝试使用 DrissionPage...")
            else:
                print(f" requests 请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f" requests 访问失败: {e}")

        return None

    def get_html_via_drission(self, url):
        """使用 DrissionPage 获取 HTML"""
        try:
            co = ChromiumOptions()
            if self.proxy:
                co.set_proxy(self.proxy)

            co.headless(True)
            page = ChromiumPage(co)

            page.get(url, timeout=60)
            print(f"DrissionPage 访问成功: {page.title}")

            html_content = page.html
            soup = BeautifulSoup(html_content, "html.parser")

            for tag in soup(["script", "style", "svg"]):
                tag.decompose()

            output = []
            for element in soup.find_all(True):
                if element.name == "a":
                    output.append(str(element))
                else:
                    output.append(element.get_text(strip=True))

            cleaned_html = "\n".join(output)
            return cleaned_html
        except Exception as e:
            print(f" DrissionPage 加载失败: {e}")
            return "获取页面失败"

    def initialize_driver(self, max_retries=3, delay=5):
        """
        尝试初始化浏览器驱动，并在失败时重试
        """
        for attempt in range(max_retries):
            try:
                if platform.system() == 'Linux':
                    co = ChromiumOptions().auto_port()
                    co.set_argument('--no-sandbox')  # 无沙盒模式
                    co.set_argument('--start-maximized')
                    co.set_argument('--headless=new')
                    co.set_proxy("http://10.9.8.118:41091")

                else:
                    co = ChromiumOptions()


                driver = WebPage(chromium_options=co)
                driver.set.scroll.smooth(on_off=False)
                driver.set.auto_handle_alert()
                return driver
            except Exception as e:
                print(f"尝试 {attempt + 1}/{max_retries} 失败: {e}")
                if attempt < max_retries - 1:  # 如果不是最后一次尝试
                    time.sleep(delay)
                    continue
                else:
                    raise e



    def get_html_content(self, url):
        """优先 requests，失败则使用 DrissionPage"""
        text = self.get_html_via_requests(url)
        if text:
            return text

        return self.get_html_via_drission(url)


def save_article_to_db(article, db_config):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    sql_insert = """
        INSERT INTO wechat_article_ai 
        (url, title, author, publish_time, content, cover_url, extra_json)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql_insert, (
        article.get("url"),
        article.get("title"),
        article.get("author"),
        article.get("publish_time"),
        article.get("content"),
        article.get("cover_url"),
        article.get("extra_json")
    ))
    conn.commit()
    cursor.close()
    conn.close()


# if __name__ == "__main__":
#     web_content = WebContent()
#     html_content = web_content.get_html_content("专业介绍｜UConn商学院王牌专业第一弹：会计学")
#     print(html_content)

if __name__ == "__main__":
    db_config = {
        "host": "10.9.8.120",
        "port": 3306,
        "user": "lgb_dbs",
        "password": "lgb123456",
        "database": "bestieu_test2",
        "charset": "utf8mb4"
    }
    url = input("请输入文章url：")
    web_content = WebContent()
    content = web_content.get_html_content(url)
    print(content)
    if content and "获取页面失败" not in content and "未找到正文" not in content:
        # 这里只做简单示例，实际可用DrissionPage提取title、author等
        article = {
            "url": url,
            "title": "",  # 可扩展自动提取
            "author": "",
            "publish_time": None,
            "content": content,
            "cover_url": "",
            "extra_json": None
        }
        save_article_to_db(article, db_config)
        print(" 已写入数据库 wechat_article_ai")
    else:
        print(" 未获取到内容，未写入数据库")
