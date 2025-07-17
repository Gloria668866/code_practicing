from playwright.sync_api import sync_playwright
import time

class PolyURegister:
    def __init__(self, email, password, surname, given_name, chinese_name, gender, birth_year,
                 nationality, nationality_province, id_card, address_country,  address_detail, mobile_number, home_phone, headless=False):
        self.email = email
        self.password = password
        self.surname = surname
        self.given_name = given_name
        self.chinese_name = chinese_name
        self.gender = gender
        self.birth_year = birth_year
        self.nationality = nationality
        self.nationality_province = nationality_province
        self.id_card = id_card
        self.address_country = address_country

        self.address_detail = address_detail
        self.mobile_number = mobile_number
        self.home_phone = home_phone
        self.headless = headless

    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = context.new_page()
            self.page = page
            self.register()
            time.sleep(5)
            browser.close()


    def register(self):
        page = self.page
        # Step 1: 打开注册页面
        page.goto("https://www38.polyu.edu.hk/eAdmission/register.do#step-1", wait_until="domcontentloaded", timeout=60000)
        # Step 2: 填写邮箱、密码、确认密码
        page.wait_for_selector('input#email')
        page.fill('input#email', self.email)
        page.fill('input#password', self.password)
        page.fill('input#confirmPassword', self.password)
        # Step 3: 点击Next
        page.click('button#next')
        time.sleep(2)

        # Step 4: 选择Student Visa
        page.wait_for_selector('a#rTypeVisa')
        page.click('a#rTypeVisa')
        # Step 5: 点击Next
        page.click('button#next')
        time.sleep(2)

        # Step 6: 填写姓名和中文名
        page.wait_for_selector('input#surname')
        page.fill('input#surname', self.surname)
        page.fill('input#givenName', self.given_name)
        page.fill('input#chineseName', self.chinese_name)


        if hasattr(self, 'gender') and self.gender:
            if self.gender.lower() == 'male':
                page.get_by_text("Male", exact=True).click()
            else:
                page.get_by_text("Female", exact=True).click()

        # 自动选择生日（2000-2008)
        if hasattr(self, 'birth_year') and self.birth_year:
            year, month, day = self.birth_year.split('-')
            page.get_by_role("button", name="event").click()
            # 动态点击左箭头，直到目标年份出现在页面
            while True:
                time.sleep(0.5)
                all_years = page.locator('div.gj-picker-bootstrap td div').all_text_contents()
                if year in all_years:
                    break
                page.locator(".gj-icon.chevron-left").click()
                time.sleep(0.5)
            page.get_by_text(year, exact=True).click()
            page.get_by_text(month, exact=True).click()
            page.get_by_text(day.lstrip('0'), exact=True).click()
            # 自动填写国籍
            def wait_for_loading(page):
                # 等待“Please Wait..”弹窗出现（如果有），再消失
                try:
                    page.wait_for_selector('text=Please Wait..', timeout=2000)
                    page.wait_for_selector('text=Please Wait..', state='detached', timeout=10000)
                except:
                    pass  # 如果没弹窗，直接跳过
            # 选择国籍
            page.locator("#nationalityCountryList_chosen a").click()
            page.locator("#nationalityCountryList_chosen .active-result").get_by_text(self.nationality,
                                                                                      exact=True).click()

            # 等待省份下拉出现
            page.wait_for_selector('#nationalityProvinceTk_chosen', state='visible', timeout=10000)
            time.sleep(0.2)
            page.locator("#nationalityProvinceTk_chosen a").click()
            page.locator("#nationalityProvinceTk_chosen .active-result").get_by_text(self.nationality_province,
                                                                                     exact=True).click()
            # 自动填写身份证号
            page.get_by_role("textbox", name="Mainland China ID Card Number").click()

            page.get_by_role("textbox", name="Mainland China ID Card Number").fill(self.id_card)

            # 地址国家
            page.locator("#addressCountryList_chosen a").click()
            page.locator("#addressCountryList_chosen").get_by_text(self.address_country, exact=True).click()


            # 取消勾选 Chinese Mainland Address Format
            page.get_by_text("Chinese Mainland Address Format").click()
            wait_for_loading(page)

            # 填写完整详细地址
            page.get_by_role("textbox", name="Address ").click()
            wait_for_loading(page)
            page.get_by_role("textbox", name="Address ").fill(self.address_detail)

            # 自动填写手机号
            page.get_by_role("textbox", name="Mobile Number").click()
            page.get_by_role("textbox", name="Mobile Number").fill(self.mobile_number)

            # 自动填写家庭电话
            page.get_by_role("textbox", name="Home Telephone Number(if").click()
            page.get_by_role("textbox", name="Home Telephone Number(if").fill(self.home_phone)

            # 勾选同意条款
            page.locator("#picsLabel").click()
            page.get_by_role("button", name="Sign Up").click()
            page.get_by_role("button", name="Yes").click()

if __name__ == "__main__":
    data = {
        "email": "zhouqiandi@163offer.com",
        "password": "YourPassword123",
        "surname": "Zhou",
        "given_name": "Qiandi",
        "chinese_name": "周乾迪",
        "gender": "Male",
        "birth_year": "2004-Aug-08",# 格式：年-月-日 生日
        "nationality": "China",#国家
        "nationality_province": "Jiangsu",#省份 这里用拼音名，首字母大写
        "id_card": "522727200408082717",# 身份证号
        "address_country": "China",# 国家
        "address_detail": "江苏省南京市鼓楼区中环国际广场",# 详细地址
        "mobile_number": "15256329878",# 手机号
        "home_phone": "13532785684"# 家庭电话
    }
    polyu = PolyURegister(**data)
    polyu.run()
