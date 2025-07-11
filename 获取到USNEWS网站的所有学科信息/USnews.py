import time
import json
from selenium import webdriver
from bs4 import BeautifulSoup
from config import MySql, obj_id

def get_total_pages(driver, url):
    driver.get(url)
    time.sleep(5)
    text = driver.page_source
    if text.strip().startswith("<html"):
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text()
    text = text.strip()
    data = json.loads(text)
    total_pages = data['data']['totalPages']
    print("总页数", total_pages)
    return total_pages

def get_items_from_text(text):
    if text.strip().startswith("<html"):
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text()
    text = text.strip()
    data = json.loads(text)
    return data['data']['items']

def main():
    url_template = "https://www.usnews.com/best-graduate-schools/api/search?format=json&program=top-business-schools&specialty=mba&_page={page}&"
    driver = webdriver.Chrome()
    first_url = url_template.format(page=1)
    total_pages = get_total_pages(driver, first_url)
    conn = MySql.get_conn()
    cursor = conn.cursor()
    seen=set()


    for page in range(1, total_pages + 1):
        url = url_template.format(page=page)
        driver.get(url)
        time.sleep(3)
        text = driver.page_source
        items = get_items_from_text(text)
        for item in items:
            school_ename = item['name']
            school_cname = ''
            country = "USA"
            try:
                #考虑到有些学校没有
                tuition = item['schoolData']['v_ft_tuition'][0][1]
            except Exception:
                tuition = ""
            business_rank = str(item['ranking']['display_rank'])+f" (学费:{tuition})"
            url_ = item['url']
            year = 2025
            school_key = f"{school_ename}_{year}"
            if school_key in seen:
                continue  # 跳过重复
            seen.add(school_key)
            id_ = obj_id.get_obj_id()
            print(f"获取第{page}页的信息：", id_, school_cname, school_ename, country, business_rank, url_, year)
            # sql = """
            # INSERT INTO usnews_school_rank (
            #     id, school_ename, school_cname, country, Business_Rank, url, year
            # ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            # """
            # cursor.execute(sql, (id_, school_ename, school_cname, country, business_rank, url_, year))

    conn.commit()
    cursor.close()
    conn.close()
    driver.quit()
    print("Business排名数据已写入数据库！")

if __name__ == '__main__':
    main()
