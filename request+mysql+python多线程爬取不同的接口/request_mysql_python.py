
from Easy_model import MySql,obj_id
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import requests

def process_one(name, school_dict):
    fakeid = get_fakeid_by_search(name)
    if fakeid:
        insert_wechat_official_account_info(name, school_dict[name], fakeid)
        print(f"已插入：{name}，fakeid={fakeid}")
    else:
        print(f"未找到fakeid：{name}")
    time.sleep(8)  # ，并发操作

def get_name_list_new():
    # 连接数据库，获取 name_list_new 和 school_dict
    conn = MySql.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, official_name,old_chinese_name,aliases FROM ai_high_school_info")
    school_rows = cursor.fetchall()
    # 2. 组装 name_list 和 school_dict
    name_list = []
    school_dict = {}  # name -> school_id
    for row in school_rows:
        school_id = row[0]
        names = set()
        if row[1]:
            names.add(row[1].strip())
        if row[2]:
            names.add(row[2].strip())
        if row[3]:
            # 支持别名为逗号分隔的多个
            for alias in row[3].split('、'):
                if alias.strip():
                    names.add(alias.strip())
        for name in names:
            name_list.append(name)
            school_dict[name] = school_id
    print("name_list:", name_list)
    # 3. 获取 wechat_official_account_info 已有的 name
    conn = MySql.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM wechat_official_account_info")
    existed_names = set(row[0].strip() for row in cursor.fetchall() if row[0])
    cursor.close()
    conn.close()

    # 4. 去重
    name_list_new = [name for name in name_list if name not in existed_names]

    return name_list_new, school_dict


def insert_wechat_official_account_info(name, school_id, biz):
    # 插入数据库
    new_id = obj_id.get_obj_id()
    sql = "INSERT INTO wechat_official_account_info (school_id, name, id, biz) VALUES (%s, %s, %s, %s)"
    val = (school_id, name,new_id , biz)
    MySql.cli_200_insert('bestieu_test2', sql, val)



def get_fakeid_by_search(school_name):
    url = "http://10.9.8.118:5001/api/search_gzh/search"

    params = {
        "keyword": school_name,
        "offset": 0,
        "num": 5
    }
    headers={
        "Accept": "application/json, text/plain, /",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection":"keep-alive",
        "Host": "10.9.8.118:5001",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
    }
    response = requests.get(url, params=params,headers=headers)
    data = response.json()
    for item in data.get("list", []):
        if item["nickname"] == school_name:
            print(f"{school_name} 的 fakeid: {item['fakeid']}")
            return item["fakeid"]
    print(f"{school_name} 未找到fakeid")
    return None
# def main():
#     name_list_new, school_dict = get_name_list_new()
#     for name in name_list_new:
#         fakeid = get_fakeid_by_search(name)
#         if fakeid:
#             insert_wechat_official_account_info(name, school_dict[name], fakeid)
#             print(f"已插入：{name}，fakeid={fakeid}")
#         else:
#             print(f"未找到fakeid：{name}")
#         time.sleep(1)  # 防止频率过高被封
#     print("全部完成！")


# 并发操作
def main():
    name_list_new, school_dict = get_name_list_new()
    with ThreadPoolExecutor(max_workers=5) as executor:  # 8个线程，可根据机器性能调整
        futures = [executor.submit(process_one, name, school_dict) for name in name_list_new]
        for future in as_completed(futures):
            pass  # 这里可以加异常处理等

    print("全部完成！")

if __name__ == "__main__":
    main()
