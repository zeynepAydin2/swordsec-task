import psycopg2
import json
import redis
import time

redis_con = redis.Redis('localhost')

postgresql_con = psycopg2.connect(
    host="localhost",
    user="postgres",
    database="example",
    password="mysecretpassword")

def record_db(usr):
	cursor = postgresql_con.cursor()

	first_name = usr[b'first_name'].decode()
	last_name = usr[b'last_name'].decode()
	email = usr[b'email'].decode()
	gender = usr[b'gender'].decode()
	ip_address = usr[b'ip_address'].decode()
	user_name = usr[b'user_name'].decode()
	agent = usr[b'agent'].decode()
	country = usr[b'country'].decode()

	cursor.execute("""INSERT INTO users(first_name, last_name, email, gender, ip_address, user_name, agent, country) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""", (first_name, last_name, email, gender, ip_address, user_name, agent, country))

	try:
		postgresql_con.commit()
		cursor.close()
		return True
	except Exception as e:
		print(e)
		return False

def listen():
	for key in redis_con.scan_iter():
		email = key.decode()
		data = redis_con.hgetall(email)
		is_recorded = record_db(data)
		if is_recorded == True:
			redis_con.delete(email)
		else:
			print("FLASE")
			pass

if __name__ == "__main__":
	while True:
		listen()
		time.sleep(10)

