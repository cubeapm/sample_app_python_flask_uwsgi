from flaskapp import create_app
import celery_tasks
from ddtrace import patch

flask_app = create_app()
patch(celery=True)
celery_app = flask_app.extensions["celery"]
