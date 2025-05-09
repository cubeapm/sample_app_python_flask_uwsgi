import requests
import socket
import time
from flask_sqlalchemy import SQLAlchemy
from flaskapp import create_app
from celery.result import AsyncResult
from celery_tasks import task_sum
from kafka import KafkaProducer, KafkaConsumer
from redis import Redis, asyncio as aioredis
from uwsgidecorators import postfork


app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql/test'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name


redis_conn = Redis(host='redis', port=6379, decode_responses=True)
aioredis_conn = aioredis.from_url("redis://redis")


@app.get("/")
def home():
    return "Hello"


@app.get("/param/<param>")
def param(param):
    return "Got param {}".format(param)


@app.route("/exception")
def exception():
    raise Exception("Sample exception")


@app.route("/api")
def api():
    requests.get('http://localhost:8000/')
    return "API called"


@app.post("/user")
# POST method for INSERT into MySQL
# curl -X POST 'http://localhost:8000/user' -d '{"name":"foo"}'
def create_user():
    user = User(name="foo")
    db.session.add(user)
    return user.to_dict()


@app.get("/user/<pk>")
def get_user(pk):
    user = User.query.get(pk)
    if not user:
        return {}
    return user.to_dict()


@app.get('/redis')
def redis():
    redis_conn.set('foo', 'bar')
    return "Redis called"


@app.get('/aioredis')
async def aioredis():
    await aioredis_conn.set('foo', 'bar')
    return "AioRedis called"


@app.get('/kafka/produce')
def kafka_produce():
    kafka_producer = KafkaProducer(
        bootstrap_servers='kafka:9092', client_id=socket.gethostname())
    kafka_producer.send('sample_topic', b'raw_bytes')
    kafka_producer.flush()
    kafka_producer.close()
    return "Kafka produced"


@app.get('/kafka/consume')
def kafka_consume():
    kafka_consumer = KafkaConsumer(
        bootstrap_servers='kafka:9092', group_id='foo', auto_offset_reset='smallest')
    kafka_consumer.subscribe(['sample_topic'])
    for msg in kafka_consumer:
        kafka_consumer.close()
        return str(msg)
    return "no message"


@app.get("/celery/task")
def start_add():
    result = task_sum.delay(1, 2)
    return {"result_id": result.id}


@app.get("/celery/result/<id>")
def task_result(id: str):
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }


@app.get("/manual")
def manual_tracing():
    do_heavy_work()
    return "Done"


def do_heavy_work():
    time.sleep(2)
