from app import flask_app
from app.extension.celery.deployer import auto_retire_inactive_heroes

celery_app = flask_app.extensions["celery"]
# Just to myself -> The command that runs the Celery app instance:
# $celery -A app.extension.celery.make_celery worker --pool solo -l info

# Triggered auto retirement task
auto_retire_inactive_heroes.delay()
