from feishu_reporter import FeishuReporter
from db_utils import get_daily_report

db_config = {
    'host': '10.9.8.120',
    'port': 3306,
    'user': 'lgb_dbs',
    'password': 'lgb123456',
    'database': 'bestieu_test2',
    'charset': 'utf8mb4'
}
webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/74956a81-0906-46c6-a2cd-dcfd0b7d6e33"

# 获取日报内容
msg = get_daily_report(db_config)

# 发送日报
reporter = FeishuReporter(webhook_url)
reporter.send(msg)