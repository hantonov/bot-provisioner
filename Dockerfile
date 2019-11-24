FROM python:3.7.4 as build

RUN apt-get update && apt-get install build-essential

COPY bot/requirements.txt /app/requirements.txt
RUN pip --no-cache-dir install -r /app/requirements.txt

COPY bot/ /app/
WORKDIR /app
CMD ["python", "app.py"]