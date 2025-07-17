
from playwright.sync_api import sync_playwright
import re
import time
import requests

from python_robots.satExamLocationTracker.test.test.testApiSat import hearders


class HongKongUniversityRegister:
    def __init__(self, email, password, alternateEmail, lastName, firstName, headless=False):
        self.email = email
        self.password = password
        self.alternateEmail = alternateEmail
        self.lastName = lastName
        self.firstName = firstName
        self.headless = headless

    def run(self, email_password):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = context.new_page()
            self.page = page
            self.visitIndex()
            self.declaration()
            self.inputData()
            browser.close()
        print("等待邮件发送...")
        time.sleep(15)  # 等待15秒再查邮件
        activation_link = self.getActivationEmail(email_password)
        if activation_link:
            print(activation_link)  # 只输出激活链接

            self.activationAccount(activation_link)

    def visitIndex(self):
        page = self.page
        page.goto("https://ug.hku.hk/hku-applicant/hku/index/login.xhtml")
        # 点击Registration按钮
        page.wait_for_selector('a:has-text("Registration")')
        page.click('a:has-text("Registration")')

    def inputData(self):
        page = self.page
        # 等待表单加载
        page.wait_for_selector('input#registration_form\\:regEmailAddr')
        # 填写表单
        page.fill('input#registration_form\\:regEmailAddr', self.email)
        page.fill('input#registration_form\\:password', self.password)
        page.fill('input#registration_form\\:retypePassword', self.password)
        page.fill('input#registration_form\\:alterEmailAddr', self.alternateEmail)
        page.fill('input#registration_form\\:surname', self.lastName)
        page.fill('input#registration_form\\:givenName', self.firstName)
        # 点击Submit按钮（用span文本定位父级button）
        page.click('button:has-text("Submit")')

    def declaration(self):
        page = self.page
        # 等待并点击复选框（同意条款）
        page.wait_for_selector('span.ui-chkbox-icon')
        page.click('span.ui-chkbox-icon')
        # 等待并点击Accept按钮
        page.wait_for_selector('button:has-text("Accept")')
        page.click('button:has-text("Accept")')



    def getActivationEmail(self, email_password):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = context.new_page()
            for i in range(3):
                try:
                    page.goto("http://mail.163offer.com/#/", wait_until="domcontentloaded", timeout=60000)
                    break
                except Exception:
                    if i == 2:
                        browser.close()
                        return
                    time.sleep(5)
            # 登录邮箱
            page.wait_for_selector('input#email')
            page.fill('input#email', self.email)
            page.fill('input#password', email_password)
            page.click('button:has-text("登录")')
            # 等待收件箱加载
            page.wait_for_selector('span.ewo-mail-list-main-view-title')
            titles = page.locator('span.ewo-mail-list-main-view-title')
            found = False
            for i in range(titles.count()):
                if "[HKU Application System] Account Activation" in titles.nth(i).inner_text():
                    titles.nth(i).click()
                    found = True
                    break
            if not found:
                browser.close()
                return None
            # 等待邮件内容加载
            page.wait_for_selector('div[data-x-div-type="body"]')
            mail_html = page.locator('div[data-x-div-type="body"]').inner_html()
            # 用正则提取激活链接
            match = re.search(r'https://ug\.hku\.hk/hku-applicant/hku/index/login\.xhtml\?id=[\w\d]+', mail_html)
            if match:
                return match.group(0)
            else:
                return None

    def activationAccount(self, activation_link):
        header = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "authorization": "4dda483855c53a6694247efb71ae855d",
            "cache-control": "no-cache",
            "cookie": "e-token=4dda483855c53a6694247efb71ae855d",
            "host": "mail.163offer.com",
            "pragma": "no-cache",
            "proxy-connection": "keep-alive",
            "referer": "http://mail.163offer.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
        }
        resp = requests.get(activation_link,headers=header)
        print("已访问激活链接，账号激活流程完成。")

if __name__ == "__main__":
    data = {
        "email": "wenruoqing@163mails.cn",
        "password": "Wrq123456789...",
        "alternateEmail": "fushiyan@163mails.cn",
        "lastName": "wen",
        "firstName": "ruoqing"
    }
    email_password = "21775878"
    hk = HongKongUniversityRegister(**data)
    hk.run(email_password)
