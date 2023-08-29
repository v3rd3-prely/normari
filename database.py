import psycopg2
import time
from datetime import datetime



def write_to_database(data):
    conn = psycopg2.connect(
        dbname="test",
        user="postgres",
        password="1234",
        host="localhost",
        port="5555"
    )
    cursor = conn.cursor()

    sql = "INSERT INTO users (id, username, email, created_at) VALUES (%s, %s, %s, %s)"

    try:
        cursor.execute(sql, data)
        conn.commit()
        print("Data inserted successfully!")
    except Exception as e:
        print("Error:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    now = datetime.now()
    time.sleep(2.1)
    print(datetime.now()-now)
    data_to_insert = (4, "user4", 'interval@gmail.com', now)
    write_to_database(data_to_insert)
