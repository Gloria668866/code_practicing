import pymysql

def get_db_connection(db_config):
    return pymysql.connect(**db_config)

def get_daily_report(db_config):
    conn = get_db_connection(db_config)
    cursor = conn.cursor()
    sql = """
    SELECT
      COUNT(DISTINCT CASE
          WHEN create_time >= CURDATE()
           AND create_time < NOW()
          THEN wx_id END) AS 今日公众号数,
      COUNT(DISTINCT CASE
          WHEN create_time >= CURDATE() - INTERVAL 1 DAY
           AND create_time < CURDATE()
          THEN wx_id END) AS 昨日公众号数,
      COUNT(CASE
          WHEN create_time >= CURDATE()
           AND create_time < NOW()
          THEN 1 END) AS 今日文章数,
      COUNT(CASE
          WHEN create_time >= CURDATE() - INTERVAL 1 DAY
           AND create_time < CURDATE()
          THEN 1 END) AS 昨日文章数,
      CASE
        WHEN COUNT(CASE
          WHEN create_time >= CURDATE() - INTERVAL 1 DAY
           AND create_time < CURDATE()
          THEN 1 END) = 0
        THEN 'N/A'
        ELSE CONCAT(
          ROUND(
            (COUNT(CASE
              WHEN create_time >= CURDATE()
               AND create_time < NOW()
              THEN 1 END) -
             COUNT(CASE
              WHEN create_time >= CURDATE() - INTERVAL 1 DAY
               AND create_time < CURDATE()
              THEN 1 END)
            ) * 100.0 /
            COUNT(CASE
              WHEN create_time >= CURDATE() - INTERVAL 1 DAY
               AND create_time < CURDATE()
              THEN 1 END),
            1
          ), '%'
        )
      END AS 文章环比增长,
      COUNT(DISTINCT wx_id) AS 累计公众号数,
      COUNT(*) AS 累计文章数
    FROM wechat_official_account_articles;
    """
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    msg = (
        f"今日采集公众号数：{row[0]}\n"
        f"昨日采集公众号数：{row[1]}\n"
        f"今日采集文章数：{row[2]}\n"
        f"昨日采集文章数：{row[3]}\n"
        f"文章环比增长：{row[4]}\n"
        f"累计采集公众号数：{row[5]}\n"
        f"累计采集文章数：{row[6]}"
    )
    return msg