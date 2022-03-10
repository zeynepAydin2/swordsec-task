# swordsec - task
## _--Upload API_
Gelen JSON dosyasındaki veriyi redise yazmamızı sağlayan Flask API.
Upload API'yi çalıştırmak için:
```sh
cd upload-api
pip install -r requirements.txt
python uploadapi.py
```
## --Redis Listener Thread
Python'da psycopg2 kütüphanesini kullanabilmek için Ubuntu üzerinde aşağıdaki kurulumların yapılması gerekir.
  ```sh
sudo apt install libpq-dev python3-dev
```
Redis Listener Thread sürekli olarak Redis'i dinleyen ve Redis'e kaydedilen dataları PostgreSQL'e aktaran python kodudur.
Çalıştırmak için:
  ```sh
cd redis-listener-thread
pip install -r requirements.txt
python listener.py
```
## --Redis Docker Kurulumu
Docker üzerinde Redis çalıştırmak için :
  ```sh
docker run --restart always --name some-redis -d -p 6379:6379 redis
```
-p parametresi kullanılarak localhost üzerinden redis container'ına ulaşılabilmektedir.
## --PostgreSQL Docker Kurulumu
PostgreSQL çalıştırmak için:
  ```sh
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres
```
## --PostgreSQL Database ve Tablo Oluşturma Adımları
 Ubuntu üzerinde postgresql-client indirmek için:
  ```sh
sudo apt-get install postgresql-client
  ```
PostgreSQL'e bilgisayarımızdan bağlanabilmek için:
```sh
psql -U postgres -W -h localhost
  ```
Bağlanılan PostgreSQL'de example database'i oluşturulur.
```sh
CREATE DATABASE example;
  ```
Oluşturulan database'e aşağıdaki gibi bağlanılır ve users tablosu oluşturulur.
```sh
psql -U postgres -W -h localhost -d example

CREATE TABLE users (
   	id SERIAL,
   	first_name VARCHAR,
	last_name VARCHAR,
	email VARCHAR,
	gender VARCHAR,
	ip_address VARCHAR,
	user_name VARCHAR,
	agent VARCHAR,
	country VARCHAR
);
  ```
PostgreSQL bağlantısından çıktık.

## --Test
**Postman üzerinden json dosyası upload-apiye gönderilir.**
**Postman üzerinden alınan örnek curl komutu :**
  ```sh
curl --location --request POST 'localhost:5000/upload-file' \
--form 'jsonfile=@"/home/zeynep/projects/swordsec/challenge-questions/backend/users/1.json"'
  ```
**PostgreSQL Kullanılarak Postgredeki Example Dbsine Bağlanılır :**
  ```sh
  psql -U postgres -W -h localhost -d example
```
**Tablonun sayısı ve içeriği aşağıdaki gibi test edilir :**
  ```sh
select count(1) from users;
select * from users;
 ```
**sistem çalıştırılmış olur.**
