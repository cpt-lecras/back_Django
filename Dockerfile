FROM python:3.12-slim-bullseye

COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

WORKDIR /app

COPY ./drfsite .
COPY ./entrypoint.sh .

RUN mkdir -p queuetask/reports
RUN chmod 777 ./entrypoint.sh


ENTRYPOINT ["./entrypoint.sh"]
