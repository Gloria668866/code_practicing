import requests
from base_reporter import DailyReporter

class FeishuReporter(DailyReporter):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, msg):
        data = {
            "msg_type": "text",
            "content": {
                "text": msg
            }
        }
        resp = requests.post(self.webhook_url, json=data)
        print(resp.text)