from flaskapp import create_app
import celery_tasks

flask_app = create_app()
celery_app = flask_app.extensions["celery"]
