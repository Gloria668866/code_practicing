from .celery_app import celery_app
from .dify_client import call_dify_api
from .db_utils import get_urls, write_sql_to_db
from .utils import get_html
import json
import time
from .db_utils import get_urls, write_sql_to_db, get_last_index_from_redis, update_last_index_to_redis

def write_teacher_info_to_db(teacher_list, url):
    print("AI返回的teacher_list：", teacher_list)
    if not teacher_list:
        sql = f"INSERT INTO wechat_task_log (url, run_time, status, teacher_count, error_msg, remark) VALUES ('{url}', NOW(), 'empty', 0, '', '');"
        write_sql_to_db(sql)
        return
    print(f"将要存入 {len(teacher_list)} 条老师信息，url: {url}")
    values = []
    for t in teacher_list:
        values.append(
            "('{org}', '{teacher_cn_name}', '{teacher_en_name}', '{position}', '{email}', '{mobile}', '{phone}', '{url}', '{wechat_name}', NOW())".format(
                org=t.get("org", ""),
                teacher_cn_name=t.get("teacher_cn_name", ""),
                teacher_en_name=t.get("teacher_en_name", ""),
                position=t.get("position", ""),
                email=t.get("email", ""),
                mobile=t.get("mobile", ""),
                phone=t.get("phone", ""),
                url=url,
                wechat_name=t.get("wechat_name", "")
            )
        )
    sql = "INSERT INTO wechat_teacher_info (org, teacher_cn_name, teacher_en_name, position, email, mobile, phone, url, wechat_name, update_time) VALUES " + ", ".join(values) + ";"
    write_sql_to_db(sql)
    print(f"✅ 已存入 wechat_teacher_info，url: {url}\n")

def process_url(url):
    html = get_html(url)
    if not html or len(html) < 100:
        print(f"网页内容获取失败，跳过：{url}")
        return
    result = call_dify_api(url)
    if result:
        try:
            ai_json = result['data']['outputs']['result']
            teacher_list = json.loads(ai_json)
            write_teacher_info_to_db(teacher_list, url)
            print("成功写入老师信息，url：", url)
        except Exception as e:
            print("解析AI返回内容失败：", e, result)
    time.sleep(5)



@celery_app.task
def batch_process():
    urls = get_urls()
    total = len(urls)
    batch_size = 100  # 你可以根据实际情况调整
    last_index = get_last_index_from_redis()
    print(f"共获取到 {total} 个URL，当前进度 {last_index}，本次处理 {batch_size} 个...")

    batch_urls = urls[last_index:last_index+batch_size]
    for url in batch_urls:
        try:
            process_url(url)
        except Exception as e:
            print("处理某个URL时出错：", e)

    new_index = last_index + batch_size
    if new_index >= total:
        new_index = 0  # 重新开始
    update_last_index_to_redis(new_index)
    print(f"本次处理结束，已更新进度到 {new_index}")