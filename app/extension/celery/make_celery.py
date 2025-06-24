from app import flask_app
from celery.schedules import crontab

celery_app = flask_app.extensions["celery"]

celery_app.conf.beat_schedule = {
    'auto-retire-inactive-heroes-every-5-mins': {
        'task': 'app.extension.celery.deployer.auto_retire_inactive_heroes',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
}
