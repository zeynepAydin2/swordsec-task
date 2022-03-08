from flask import Flask, request
import json
import redis

app = Flask(__name__)
conn = redis.Redis('localhost')

@app.route('/upload-file', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		jsonfile = request.files['jsonfile']
		file_data = json.load(jsonfile)
		error_list = []
		for i in file_data:
			tmp = conn.hmset(i['email'], i)
			if tmp == False:
				error_list.append(i['id'])
		if len(error_list) != 0:
			return str(error_list), 500	
		else:
			return "success", 200
	else:
		return "bad request", 400
  
if __name__ == '__main__':
    app.run()
