import psycopg2
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

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    data_to_insert = (3, "user3", 'elloonemore@gmail.com', now)
    write_to_database(data_to_insert)
