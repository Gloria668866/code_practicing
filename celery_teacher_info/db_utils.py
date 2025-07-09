import pymysql
import redis
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
        print(f"⚠ SQL不合法，跳过。内容：{sql}")
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


REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 3  # 建议用一个空闲的db
PROGRESS_KEY = 'wechat_task_progress'

def get_last_index_from_redis():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    value = r.get(PROGRESS_KEY)
    return int(value) if value else 0

def update_last_index_to_redis(new_index):
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    r.set(PROGRESS_KEY, new_index)