FROM ubuntu:22.04

RUN apt-get update && apt-get install -y gcc libffi-dev python3-pip

WORKDIR /flask

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uwsgi", "--http", ":8000", "--wsgi-file", "app.py", "--callable", "app", "--master", "-p", "4", "--enable-threads", "--need-app"]
