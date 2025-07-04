class DailyReporter:
    def get_report(self):
        raise NotImplementedError("子类必须实现get_report方法")

    def send(self, msg):
        raise NotImplementedError("子类必须实现send方法")