from flaskapp import create_app
import celery_tasks
from ddtrace import patch_all

flask_app = create_app()
patch_all()
celery_app = flask_app.extensions["celery"]
