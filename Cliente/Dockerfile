FROM bitnami/python:3.8.13

RUN pip install cassandra-driver

EXPOSE 5000
COPY . .
CMD ["python", "app.py"]