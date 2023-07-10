import datetime
import random
import math
import pika
import json
import random
import time
import numpy as np
from scipy.stats import norm

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


# Число сгенерить из промежутка с нормальным распределением в его центре
def get_gauss_number(min, max, sigma):
    center = (max + min) / 2
    number = np.random.normal(center, sigma, 1)[0]
    if not min <= number <= max:
        number = center
    return number


# Датчик температуры
def sensor(sensor_id, start_date, end_date, delta):
    delta_num = delta.total_seconds() // 60
    oven_temperature = 0
    block_time = 0
    warm_time = 0
    work_time = 0
    temp_amp_work = 0

    # Коэффициенты для рассчета времени нагрева и остывания в зависимости от max температуры печи
    k_warming_temp = 0.6

    current_date = start_date
    while current_date <= end_date:
        month = current_date.month
        hour = current_date.hour
        minute = current_date.minute

        # Базовая температура в зависимости от месяца
        base_temp = {
            1: 24,
            2: 23.9,
            3: 23.7,
            4: 22.6,
            5: 21,
            6: 19.3,
            7: 18.7,
            8: 20,
            9: 22.8,
            10: 24.9,
            11: 25.7,
            12: 24.7,
        }[month]

        # Дневное колебание температуры по минутам входе дня и ночи
        temp_amp = 7 * math.sin(2 * math.pi * (hour * 60 + minute - 600) / 1440)

        # Случайное колебание температуры +-0.9 градуса
        rand_temp_amp = random.uniform(-0.9, 0.9)

        # Эмуляция работы печи
        if block_time <= 0:
            # Рассчет момента начала работы печи 3 нормальных распределения в завтрак/обед/ужин
            mu = 0  # мат ожидание(центр распределения)
            sigma = 50  # стандартное отклонение в минутах
            # [mu +- sigma]  промежуток с вероятностью попасть 68%

            if 0 <= hour < 5:
                mu = 7.5 * 60
            elif 5 <= hour < 11:
                mu = 7.5 * 60
            elif 11 <= hour < 17:
                mu = 13.5 * 60
            elif 17 <= hour < 24:
                mu = 19.5 * 60

            time_in_minutes = hour * 60 + minute
            area = norm.cdf(time_in_minutes, mu, sigma) - norm.cdf(time_in_minutes - 5, mu, sigma)

            # Начало работы печи в if
            x = random.uniform(0, 1)
            if x < area:
                # print("START============================================================================")
                pick_temperature = get_gauss_number(min=90, max=200, sigma=55)
                delta_temperature = pick_temperature - oven_temperature
                warm_time = k_warming_temp * delta_temperature
                work_time = get_gauss_number(min=20, max=150, sigma=30)
                # cool_time = k_cooling_temp * delta_temperature
                block_time = warm_time + work_time + get_gauss_number(min=20, max=150, sigma=30)
                # print("WORK", pick_temperature, warm_time/60, work_time/60, cool_time/60, block_time / 60, hour, minute)
        else:
            # Нагрев (равномерный на всем промежутке) и работа
            block_time -= delta_num
            if warm_time > 0:
                warm_time -= delta_num
                oven_temperature += 5 * (1 / k_warming_temp)
                # print("WARMING==========================================")
            elif work_time > 0:
                work_time -= delta_num
                # print("COOKING==========================================")

        # Остывание печи до момента полного остывания или нового запуска печи
        # Остывает не равномерно
        if oven_temperature > 0 and work_time <= 0 and warm_time <= 0:
            oven_temperature -= 5 * random.uniform(1.3, 1.7)
            if oven_temperature < 0:
                oven_temperature = 0
                # print("COOLING==========================================")

        # Колебания в ходе работы печи при max температуре
        if work_time > 0:
            temp_amp_work = random.uniform(-3, 3)
        else:
            temp_amp_work = 0

        # Итоговая температура
        current_temperature = base_temp + temp_amp + oven_temperature + temp_amp_work + rand_temp_amp
        # print(f"{sensor_id}  {current_date.strftime('%d.%m.%Y %H:%M:%S')}  {current_temperature}°C  {
        # oven_temperature}")

        # Записываем в очердь 
        data = {"temperature": current_temperature, "date": current_date.strftime('%Y-%m-%d %H:%M:%S'), "id": sensor_id}
        message = json.dumps(data)
        send_message(message)

        current_date += delta


def send_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT,
        virtual_host='/', credentials=pika.PlainCredentials(
            RABBITMQ_USER, RABBITMQ_PASSWORD)))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME,
                          body=str(message))
    connection.close()


def main():
    sensor_number = 5  # better be 1000 but so slow...
    start_date = datetime.datetime(2023, 1, 1, 0, 0, 0)
    end_date = datetime.datetime(2023, 1, 31, 23, 55, 0)
    delta = datetime.timedelta(minutes=5)

    for sensor_id in range(sensor_number):
        sensor(sensor_id + 1, start_date, end_date, delta)


if __name__ == "__main__":
    main()
    print("Complited successfully.")
