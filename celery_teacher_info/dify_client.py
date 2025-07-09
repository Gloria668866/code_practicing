import requests
import time

DIFY_API_URL = "http://10.9.8.120:9988/v1/workflows/run"
DIFY_API_KEY = "app-mXpyuHNkqoiXhiKdIZFFVMYy"
WORKFLOW_ID = "34ff25ee-5de7-4d3f-8642-ce2df7b6ce88"
APP_ID = "34ff25ee-5de7-4d3f-8642-ce2df7b6ce88"
USER_ID = "test_user"
headers = {
    "Authorization": f"Bearer {DIFY_API_KEY}",
    "Content-Type": "application/json",
}

def call_dify_api(url, retry=3):
    data = {
        "workflow_id": WORKFLOW_ID,
        "inputs": {"url": url},
        "user": USER_ID,
        "app_id": APP_ID,
        "response_mode": "blocking",
    }
    for i in range(retry):
        try:
            response = requests.post(DIFY_API_URL, headers=headers, json=data, timeout=300)
            if response.status_code == 429:
                print("被限流，等待5秒重试...")
                time.sleep(5)
                continue
            if response.status_code == 200:
                result = response.json()
                print("✅ Dify返回：", result)
                return result
            else:
                print(f"❌ Dify请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Dify请求异常: {e}")
            time.sleep(5)
    return None