from flaskapp import create_app
from elasticapm import Client, instrument
from elasticapm.contrib.celery import register_instrumentation, register_exception_tracking
import celery_tasks

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

apm_client = Client()

instrument()
register_exception_tracking(apm_client)
register_instrumentation(apm_client)
