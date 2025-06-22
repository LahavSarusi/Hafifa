from app import flask_app

celery_app = flask_app.extensions["celery"]
# Just to myself -> The command that runs the Celery app instance:
# celery -A app.extension.celery.make_celery worker --pool solo -l info
