import os

from celery.schedules import crontab

broker_url = os.environ.get("CELERY_BROKER_URL", 'redis://localhost:6379')
result_backend = os.environ.get("CELERY_RESULT_BACKEND", 'redis://localhost:6379')

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Berlin'
enable_utc = True

task_routes = {
    'tasks.fetch_daily_data': {'rate_limit': '10/m'}
}

beat_schedule = {
    'fetch-every-day': {
        'task': 'tasks.fetch_daily_data',
        'schedule': crontab(minute=21, hour=20),
    },
}
