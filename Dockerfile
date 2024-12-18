FROM python:3.12.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ARG VERSION
RUN echo $VERSION > /app/bot/version.txt

CMD ["python", "bot/bot.py"]
