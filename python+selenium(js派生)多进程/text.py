
# 文件名：wechat_auto_add.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Easy_model import MySql, obj_id
from multiprocessing import Pool

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# ================== 配置区 ==================
CHROME_DRIVER_PATH = r'C:\Users\Administrator\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'  # 你的chromedriver路径
PAGE_URL = 'http://10.9.8.118:5001/#/crawler'  # 你的页面url
HEADLESS = True  # True为无界面，False为可视化调试
WAIT_TIME = 20  # 显式等待时间
SLEEP_BETWEEN = 10  # 每个学校间隔秒数

def process_school_batch(school_batch):
    auto_add_wechat_official_accounts(
        school_batch,
        chrome_driver_path=CHROME_DRIVER_PATH,
        page_url=PAGE_URL,
        headless=HEADLESS
    )
# 1. 点击“+”号
js_click_plus = '''
var el = document.querySelector("#app > div > div > div.p-2.sm\\\\:p-4.wp-transition > div > div.grid.grid-cols-2.lg\\\\:grid-cols-4.gap-4 > div:nth-child(1) > div.flex.justify-between.items-center.mb-4 > div > div:nth-child(2) > svg > path");
if(el){ el.parentElement.dispatchEvent(new MouseEvent('click', {bubbles:true})); }
'''

# 2. 输入公众号关键词
js_input_keyword = '''
var input = document.querySelector("body > div.v-binder-follower-container > div > div > div.n-popover__content > div > div.n-input.n-input--resizable.n-input--stateful > div.n-input-wrapper > div.n-input__input > input");
if(input){
    input.value = arguments[0];
    input.dispatchEvent(new Event('input', {bubbles:true}));
}
'''

# 3. 点击“下一页”
js_click_next = '''
var btn = document.querySelector("body > div.v-binder-follower-container > div > div > div.n-popover__content > div > div.flex.justify-center.items-center.space-x-2 > button:nth-child(3)");
if(btn){ btn.dispatchEvent(new MouseEvent('click', {bubbles:true})); }
'''

# 4. 匹配公众号（判断是否有匹配结果）


js_get_all_names = '''
return Array.from(document.querySelectorAll('span.text-sm'))
    .map(x => x.innerText.trim());
'''

# 5. 选择公众号后，点击文章链接搜索
js_click_article_search = '''
var el = document.querySelector("#el-id-5482-7 > label.el-radio-button.is-active.el-radio-button--small > span");
if(el){ el.dispatchEvent(new MouseEvent('click', {bubbles:true})); }
'''

# 6. 数量改为1000

js_set_num_1000 = '''
var inputs = document.querySelectorAll('input.el-input__inner[type="number"]');
if(inputs.length >= 2){
    var input = inputs[1];
    input.value = 1000;
    input.setAttribute('aria-valuenow', 1000);
    input.dispatchEvent(new Event('input', {bubbles:true}));
    input.dispatchEvent(new Event('change', {bubbles:true}));
    input.blur();
}
'''

# 7. 点击“创建”
js_click_create = '''
var el = document.querySelector("#app > div > div > div.p-2.sm\\\\:p-4.wp-transition > div > div.grid.grid-cols-2.lg\\\\:grid-cols-4.gap-4 > div:nth-child(2) > div.flex.justify-between.items-center.mb-4 > button > div > span");
if(el){ el.dispatchEvent(new MouseEvent('click', {bubbles:true})); }
'''

# 8. 点击“文章内容”
js_click_article_content = '''
var el = document.querySelector("#app > div > div > div.p-2.sm\\\\:p-4.wp-transition > div > div.grid.grid-cols-2.lg\\\\:grid-cols-4.gap-4 > div:nth-child(3) > div.flex.justify-between.items-center.mb-4 > button > div > span");
if(el){ el.dispatchEvent(new MouseEvent('click', {bubbles:true})); }
'''

# 9. 点击“开始”
js_click_start = '''
var el = document.querySelector("#app > div > div > div.p-2.sm\\\\:p-4.wp-transition > div > div.w-full.wp-card.py-4.px-2.sm\\\\:px-4.rounded.sm\\\\:rounded-xl.wp-transition > div.flex.justify-between.items-center.mb-4.h-8 > div.flex.justify-between.items-center > div:nth-child(2) > button > div > span");
if(el){ el.dispatchEvent(new MouseEvent('click', {bubbles:true})); }
'''
js_click_home = '''
var btn = document.querySelector('body > div:nth-child(4) > div > div > div.n-popover__content > div > div.flex.justify-center.items-center.space-x-2 > button:nth-child(1)');
if(btn){ btn.dispatchEvent(new MouseEvent('click', {bubbles:true})); }
'''
# 新增：点击第N个公众号的JS函数
js_click_select_first = '''
var el = document.querySelector('span.el-radio__label');
if(el){ el.dispatchEvent(new MouseEvent('click', {bubbles:true})); }
'''


def js_click_nth_option(idx):
    return f'''
    var spans = Array.from(document.querySelectorAll('span.text-sm'));
    if(spans[{idx}]){{
        var parent = spans[{idx}].parentElement;
        if(parent) {{
            parent.dispatchEvent(new MouseEvent('click', {{bubbles:true}}));
        }}
    }}
    '''

# ================== 数据库处理 ==================
def get_name_list_new():
    conn = MySql.get_conn()#这里数据库再另外一个类，看实际情况自己改写,这里就不上传了
    cursor = conn.cursor()
    cursor.execute("SELECT id, official_name,old_chinese_name,aliases FROM ai_high_school_info")
    school_rows = cursor.fetchall()
    name_list = []
    school_dict = {}
    for row in school_rows:
        school_id = row[0]
        names = set()
        if row[1]:
            names.add(row[1].strip())
        if row[2]:
            names.add(row[2].strip())
        if row[3]:
            for alias in row[3].split('、'):
                if alias.strip():
                    names.add(alias.strip())
        for name in names:
            name_list.append(name)
            school_dict[name] = school_id
    cursor.close()
    conn.close()

    # 去除已存在的
    conn = MySql.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM wechat_official_account_info")
    existed_names = set(row[0].strip() for row in cursor.fetchall() if row[0])
    cursor.close()
    conn.close()
    name_list_new = [name for name in name_list if name not in existed_names]
    return name_list_new, school_dict

# ================== 自动化主流程 ==================
def auto_add_wechat_official_accounts(name_list, chrome_driver_path, page_url, headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--lang=zh-CN')
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(page_url)
    wait = WebDriverWait(driver, WAIT_TIME)

    MAX_PAGE = 1  # 建议设大一点

    for school_name in name_list:
        try:
            print(f"正在添加：{school_name}")
            driver.execute_script(js_click_plus)
            time.sleep(3)
            driver.execute_script(js_input_keyword, school_name)
            time.sleep(3)
            driver.execute_script(js_click_home)
            time.sleep(3)

            found = False
            for page in range(MAX_PAGE):
                names = driver.execute_script(js_get_all_names)

                for n in names:
                    print("  -", n)
                matched_idx = -1
                for idx, name in enumerate(names):
                    if school_name in name or name in school_name:
                        matched_idx = idx
                        break
                if matched_idx != -1:
                    driver.execute_script(js_click_nth_option(matched_idx))
                    time.sleep(3)
                    driver.execute_script(js_click_select_first)
                    time.sleep(3)
                    driver.execute_script(js_set_num_1000)
                    inputs = driver.find_elements(By.CSS_SELECTOR, 'input.el-input__inner[type="number"]')
                    if len(inputs) >= 2:
                        num_input = inputs[1]
                        num_input.clear()
                        num_input.send_keys('1000')
                        num_input.send_keys(Keys.ENTER)
                        time.sleep(3)
                    else:
                        print("没有找到数量输入框！")
                    print(f"{school_name} 匹配成功，已点击公众号并选择，数量设置为1000，任务创建并完成成功")
                    found = True
                    break
                else:
                    # 判断“下一页”按钮是否可用
                    next_btn = driver.execute_script('''
                        var btn = document.querySelector('button.text-orange-600.bg-orange-100');
                        return btn && !btn.disabled;
                    ''')
                    if next_btn:
                        driver.execute_script(js_click_next)
                        time.sleep(3)
                    else:
                        break
            if not found:
                print(f"{school_name} 没有匹配，换下一个")
                continue
            if found:
            # 后续流程（只需执行一次）
                driver.execute_script(js_click_article_search)
                time.sleep(3)
                driver.execute_script(js_set_num_1000)
                time.sleep(3)
                driver.execute_script(js_click_create)
                time.sleep(3)
                driver.execute_script(js_click_article_content)
                time.sleep(3)
                driver.execute_script(js_click_start)
                print(f"{school_name} 添加成功")
                time.sleep(3)
        except Exception as e:
                print(f"{school_name} 添加失败: {e}")
                continue

# ================== 主入口 ==================
if __name__ == "__main__":
    # name_list_new, school_dict = get_name_list_new()
    # auto_add_wechat_official_accounts(
    #     name_list_new,
    #     chrome_driver_path=CHROME_DRIVER_PATH,
    #     page_url=PAGE_URL,
    #     headless=HEADLESS)

    name_list_new, school_dict = get_name_list_new()
    # 分批
    batch_size = 10  # 每个进程处理10个学校，可根据机器性能调整
    batches = [name_list_new[i:i + batch_size] for i in range(0, len(name_list_new), batch_size)]
    pool = Pool(processes=3)  # 3个进程，可根据CPU核数调整
    pool.map(process_school_batch, batches)
    pool.close()
    pool.join()
