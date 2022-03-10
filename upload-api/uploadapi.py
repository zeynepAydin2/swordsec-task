from flask import Flask, request
import json
import redis

# flask app olusturuldu.
app = Flask(__name__)

# Redise connection olusturuldu.
conn = redis.Redis('localhost')

# /upload-api endpointi
@app.route('/upload-file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # request icerisindeki dosya alindi
        jsonfile = request.files['jsonfile']
        
        # Dosya icerigi json'a cevirildi.
        file_data = json.load(jsonfile)

        # hata ile karsilasilmasi durumunda kullaniciya donulecek id listesi
        error_list = []

        # dosya icerigindeki her bir veri redise yazilir
        for i in file_data:
            tmp = conn.hmset(i['email'], i)ı

            # redise yazilamamasi durumunda id error_list e eklenir
            if tmp == False:
                error_list.append(i['id'])
        
        # error_list bos degilse 500 bos ise 200 
        if len(error_list) != 0:
            return str(error_list), 500 
        else:
            return "success", 200
    else:
        return "bad request", 400
  
if __name__ == '__main__':
    app.run()
