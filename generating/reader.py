import pika
import json
import csv
import datetime
 
# Параметры подключения к RabbitMQ
with open('rabbit_config.json') as f:
    config = json.load(f)
 
rabbitmq_config = config['rabbitmq']
RABBITMQ_HOST = rabbitmq_config['host']
RABBITMQ_PORT = rabbitmq_config['port']
RABBITMQ_USER = rabbitmq_config['user']
RABBITMQ_PASSWORD = rabbitmq_config['password']
 
# Параметры очереди RabbitMQ
QUEUE_NAME = rabbitmq_config['queue_name']
 
 
# Функция, которая обрабатывает сообщение из очереди RabbitMQ
with open('temperature.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    def process_message(ch, method, properties, body):
        parsed_data = json.loads(body)
 
        temperature = parsed_data['temperature']
        date = parsed_data['date']
        sensor_id = parsed_data['id']
        # print(f"{sensor_id}  {date}  {round(temperature, 1)}°C")
        writer.writerow([sensor_id, date, round(temperature, 1)])
 
 
    # Подключение к очереди RabbitMQ и получение сообщений
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT,
        virtual_host='/', credentials=pika.PlainCredentials(
            RABBITMQ_USER, RABBITMQ_PASSWORD)))
 
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message, auto_ack=True)
    channel.start_consuming()