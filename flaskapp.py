from celery import Celery, Task
from flask import Flask
import newrelic.agent


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://redis",
            result_backend="redis://redis",
            task_ignore_result=True,
        ),
    )
    celery_init_app(app)
    return app


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            # When using custom task class, we may need to add the
            # below line for New Relic to work properly.
            with newrelic.agent.BackgroundTask(
                application=newrelic.agent.application(),
                name=self.name,
                group='Celery'
            ):
                with app.app_context():
                    return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    # celery_app = Celery(app.name)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
