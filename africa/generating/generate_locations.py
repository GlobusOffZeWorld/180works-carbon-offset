import json
import numpy as np
import psycopg2


with open('rabbit_config.json') as f:
    config = json.load(f)

# Параметры подключения к Postgres
postgres_config = config['postgres']
POSTGRES_HOST = postgres_config['host']
POSTGRES_PORT = postgres_config['port']
POSTGRES_DBNAME = postgres_config['dbname']
POSTGRES_USER = postgres_config['user']
POSTGRES_PASSWORD = postgres_config['password']

# Параметры таблицы в Postgres
TABLE_NAME = 'locations'


def main():
    sensor_number = 1000

    # Подключение к Postgres и вставка данных в таблицу
    conn = psycopg2.connect(
        host=POSTGRES_HOST, port=POSTGRES_PORT, dbname=POSTGRES_DBNAME,
        user=POSTGRES_USER, password=POSTGRES_PASSWORD
    )
    cur = conn.cursor()

    for sensor_id in range(sensor_number):
        district = np.random.randint(1, 29)
        insert_query = f"INSERT INTO {TABLE_NAME} (id_stove, id_district) VALUES (%s, %s)"
        cur.execute(insert_query, (sensor_id + 1, district))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
    print("Complited successfully.")

