from celery.signals import worker_process_init
from flaskapp import create_app
from tracing import init_tracing
import celery_tasks

from opentelemetry.instrumentation.celery import CeleryInstrumentor

flask_app = create_app()
celery_app = flask_app.extensions["celery"]


@worker_process_init.connect(weak=False)
def init_celery_tracing(*args, **kwargs):
    init_tracing()
    CeleryInstrumentor().instrument()
    # Additional instrumentation can be enabled by
    # following the docs for respective instrumentations at
    # https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation
