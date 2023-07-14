import datetime
import math
import pika
import json
import time
import numpy as np
from scipy.stats import norm
import psycopg2

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


# result = {}

# Число сгенерить из промежутка с нормальным распределением в его центре
def get_gauss_number(min, max, sigma):
    center = (max + min) / 2
    number = np.random.normal(center, sigma, 1)[0]
    if not min <= number <= max:
        number = center
    return number


# Датчик температуры
def sensor(sensor_id, start_date, end_date, delta, mu_values, base_temp_values):
    delta_num = delta.total_seconds() // 60
    oven_temperature = 0
    block_time = 0
    warm_time = 0
    work_time = 0
    temp_amp_work = 0

    # it_worked = False

    # Коэффициенты для рассчета времени нагрева и остывания в зависимости от max температуры печи
    k_warming_temp = 0.6

    mu = 0  # мат ожидание(центр распределения)
    sigma = 50  # стандартное отклонение в минутах

    current_date = start_date
    while current_date <= end_date:
        month = current_date.month
        hour = current_date.hour
        minute = current_date.minute

        # if hour == minute == 0:
        #     it_worked = False

        # Базовая температура в зависимости от месяца
        base_temp = base_temp_values[month - 1]

        # Дневное колебание температуры по минутам входе дня и ночи
        temp_amp = 7 * math.sin(2 * math.pi * (hour * 60 + minute - 600) / 60 * 24)

        # Случайное колебание температуры +-0.9 градуса
        rand_temp_amp = np.random.uniform(-0.9, 0.9)

        # Эмуляция работы печи
        if block_time <= 0:
            # Рассчет момента начала работы печи 3 нормальных распределения в завтрак/обед/ужин
            mu = mu_values[hour]

            time_in_minutes = hour * 60 + minute
            area = norm.cdf(time_in_minutes, mu, sigma) - norm.cdf(time_in_minutes - delta_num, mu, sigma)

            # Начало работы печи в if
            x = np.random.uniform(0, 1)
            if x < area:
                # if not it_worked:
                #     it_worked = True
                #     result[current_date.date()][0] += 1
                # result[current_date.date()][1] += 1

                pick_temperature = get_gauss_number(min=90, max=200, sigma=55)
                delta_temperature = pick_temperature - oven_temperature
                warm_time = k_warming_temp * delta_temperature
                work_time = get_gauss_number(min=20, max=150, sigma=30)
                block_time = warm_time + work_time + get_gauss_number(min=20, max=150, sigma=30)

                # result[current_date.date()][2] += (warm_time + work_time) / 60
        else:
            # Нагрев (равномерный на всем промежутке) и работа
            block_time -= delta_num
            if warm_time > 0:
                warm_time -= delta_num
                oven_temperature += delta_num * (1 / k_warming_temp)
            elif work_time > 0:
                work_time -= delta_num

        # Остывание печи до момента полного остывания или нового запуска печи
        # Остывает не равномерно
        if oven_temperature > 0 and work_time <= 0 and warm_time <= 0:
            oven_temperature -= delta_num * np.random.uniform(1.3, 1.7)
            if oven_temperature < 0:
                oven_temperature = 0

                # Колебания в ходе работы печи при max температуре
        if work_time > 0:
            temp_amp_work = np.random.uniform(-3, 3)
        else:
            temp_amp_work = 0

        # Итоговая температура
        current_temperature = base_temp + temp_amp + oven_temperature + temp_amp_work + rand_temp_amp

        # Записываем в очердь
        data = {"temperature": current_temperature, "date": current_date.strftime('%d.%m.%Y %H:%M:%S'), "id": sensor_id}
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
    # Температура по месяцам
    base_temp_values = [24, 23.9, 23.7, 22.6, 21, 19.3, 18.7, 20, 22.8, 24.9, 25.7, 24.7]

    # Центры распределений в зависимости от времени суток
    mu_values = [7.5 * 60] * 11 + [13.5 * 60] * 6 + [19.5 * 60] * 7

    sensor_number = 100
    start_date = datetime.datetime(2023, 3, 1, 0, 0, 0)
    end_date = datetime.datetime(2023, 3, 31, 23, 55, 0)
    delta = datetime.timedelta(minutes=15)

    # cur_date = start_date
    # while cur_date <= end_date:
    #     result[cur_date.date()] = [0, 0, 0]
    #     cur_date += datetime.timedelta(days=1)

    for sensor_id in range(sensor_number):
        sensor(sensor_id + 1, start_date, end_date, delta, mu_values, base_temp_values)

    # with open('result.txt', 'w', newline='') as fw:
    #     fw.write(f"Date,Stoves_num,Work_num,Work_time\n")
    #     for r in result:
    #         fw.write(f"{r},{result[r][0]},{result[r][1]},{round(result[r][2], 2)}\n")


if __name__ == "__main__":
    start_time = time.perf_counter()

    main()

    end_time = time.perf_counter()

    print(f"Time: {end_time - start_time} sec")
    print("Complited successfully.")
