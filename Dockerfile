FROM python:3

RUN mkdir /app
COPY ./ /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]