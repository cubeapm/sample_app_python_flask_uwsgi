from flaskapp import create_app
from celery.signals import worker_process_init
import celery_tasks
import newrelic.agent

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

@worker_process_init.connect(weak=False)
def init_celery_tracing(*args, **kwargs):
    newrelic.agent.initialize()
