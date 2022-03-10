import psycopg2
import json
import redis
import time

# Redis connection
redis_con = redis.Redis('localhost')

# PostgreSQL connection
postgresql_con = psycopg2.connect(
    host="localhost",
    user="postgres",
    database="example",
    password="mysecretpassword")

def record_db(usr):
    cursor = postgresql_con.cursor()
    
    # usr objesindeki her bir value icin byte -> str yapilir.
    first_name = usr[b'first_name'].decode()
    last_name = usr[b'last_name'].decode()
    email = usr[b'email'].decode()
    gender = usr[b'gender'].decode()
    ip_address = usr[b'ip_address'].decode()
    user_name = usr[b'user_name'].decode()
    agent = usr[b'agent'].decode()
    country = usr[b'country'].decode()

    # data postgresqle insert edilir.
    cursor.execute("""INSERT INTO users(first_name, last_name, email, gender, ip_address, user_name, agent, country) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""", (first_name, last_name, email, gender, ip_address, user_name, agent, country))
    
    try:
        # insert komutu commit edilir
        postgresql_con.commit()
        cursor.close()
        return True
    except Exception as e:
        # commit esnasinda hata ile karsilasilirsa False doner
        print(e)
        return False

def listen():
    # scan_iter metodu ile redis'de bulunan tum keyler alinir
    for key in redis_con.scan_iter():
        
        # email byte -> str
        email = key.decode()
        
        # key icin data okunur
        data = redis_con.hgetall(email)

        # postgresql'e yazilmak uzere record_db fonksiyonuna gonderilir
        is_recorded = record_db(data)

        # Veriler kaydedilmisse silinir.
        if is_recorded == True:
            redis_con.delete(email)
        else:
            pass

if __name__ == "__main__":
    # her 10 saniyede redis kontrol edilir.
    while True:
        listen()
        time.sleep(10)

