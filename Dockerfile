FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt /app
RUN python3 -m pip install -r requirements.txt
RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY . /app

CMD python3 main.py