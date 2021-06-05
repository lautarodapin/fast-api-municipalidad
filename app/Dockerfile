FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY . /app/

CMD uvicorn main:app --host 0.0.0.0 --port $PORT