import pika
import json
import psycopg2
from datetime import datetime

# Параметры подключения к RabbitMQ
with open('rabbit_config.json') as f:
    config = json.load(f)

rabbitmq_config = config['rabbitmq']
RABBITMQ_HOST = rabbitmq_config['host']
RABBITMQ_PORT = rabbitmq_config['port']
RABBITMQ_USER = rabbitmq_config['user']
RABBITMQ_PASSWORD = rabbitmq_config['password']

# Параметры подключения к Postgres
postgres_config = config['postgres']
POSTGRES_HOST = postgres_config['host']
POSTGRES_PORT = postgres_config['port']
POSTGRES_DBNAME = postgres_config['dbname']
POSTGRES_USER = postgres_config['user']
POSTGRES_PASSWORD = postgres_config['password']

QUEUE_NAME = rabbitmq_config['queue_name']

# Параметры таблицы в Postgres
TABLE_NAME = 'raw_temperature'


# Функция, которая обрабатывает сообщение из очереди RabbitMQ
def process_message(ch, method, properties, body):
    parsed_data = json.loads(body)

    temperature = parsed_data['temperature']
    date = parsed_data['date']
    sensor_id = parsed_data['id']

    # Подключение к Postgres и вставка данных в таблицу
    conn = psycopg2.connect(
        host=POSTGRES_HOST, port=POSTGRES_PORT, dbname=POSTGRES_DBNAME,
        user=POSTGRES_USER, password=POSTGRES_PASSWORD
    )
    cur = conn.cursor()

    insert_query = f"INSERT INTO {TABLE_NAME} (id_stove, date, temperature) VALUES (%s, %s, %s)"
    cur.execute(insert_query, (sensor_id, date, round(temperature, 1)))

    conn.commit()
    cur.close()
    conn.close()


# Подключение к очереди RabbitMQ и получение сообщений
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST, port=RABBITMQ_PORT,
    virtual_host='/', credentials=pika.PlainCredentials(
        RABBITMQ_USER, RABBITMQ_PASSWORD)))

channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message, auto_ack=True)
channel.start_consuming()
