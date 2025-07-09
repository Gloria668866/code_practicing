from celery import Celery
from celery.schedules import crontab

backend = 'redis://127.0.0.1:6379/1'
broker = 'redis://127.0.0.1:6379/2'

celery_app = Celery(
    'celery_teacher_info',
    backend=backend,
    broker=broker,
    include=['celery_teacher_info.tasks']  # 让Celery主动导入任务模块
)
celery_app.conf.timezone = 'Asia/Shanghai'

celery_app.conf.beat_schedule = {
    'run-every-5-minutes': {
        'task': 'celery_teacher_info.tasks.batch_process',
        'schedule': crontab(minute=0),  # 每一小时跑100个url
    },
}