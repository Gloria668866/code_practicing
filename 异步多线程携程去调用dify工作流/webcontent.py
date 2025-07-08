
import requests,platform
from bs4 import BeautifulSoup
from DrissionPage import ChromiumPage, ChromiumOptions,WebPage
import time

class WebContent:
    def __init__(self, proxy=None):
        """初始化 WebContent"""
        self.proxy = proxy or "http://10.9.8.118:41091"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Referer": "https://www.google.com/",
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1"
        }

    def get_html_via_requests(self, url):
        """尝试使用 requests 获取 HTML"""
        try:
            proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
            response = requests.get(url, headers=self.headers, proxies=proxies, timeout=10, verify=False)

            if response.status_code == 200:
                html_text = response.text
                print(f" requests 获取成功，页面长度: {len(html_text)}")

                if len(html_text) >= 500:
                    soup = BeautifulSoup(html_text, "html.parser")
                    cleaned_html = soup.text.replace("\n", "")
                    print(f"处理后的 HTML 页面长度: {len(cleaned_html)}")
                    return cleaned_html
                else:
                    print("⚠️ requests 获取的内容太短，尝试使用 DrissionPage...")
            else:
                print(f"❌ requests 请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ requests 访问失败: {e}")

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
            print(f" DrissionPage 访问成功: {page.title}")

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
            print(f"❌ DrissionPage 加载失败: {e}")
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
        # text = self.get_html_via_requests(url)
        # if text:
        #     return text

        return self.get_html_via_drission(url)


if __name__ == "__main__":
    web_content = WebContent()
    html_content = web_content.get_html_content("专业介绍｜UConn商学院王牌专业第一弹：会计学")
    print(html_content)
