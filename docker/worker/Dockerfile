FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["rq", "worker", "task_queue", "--url", "redis://tcc-redis:6379/0"]
