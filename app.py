from flask import Flask
from flask import render_template
from flask import jsonify, request
app = Flask(__name__)

@app.route('/')
def my_first_route():
	return "<h1> Hello World! </h1>"

@app.route('/route/<name>')
def my_second_route(name):
     return name

@app.route('/get_users', methods=['GET'])
def get_all_users():
    if request.method == 'GET':
	    return jsonify({'status': 'success', 'data':  ['aria', 'tim', 'varun', 'alex']})
    else:
        return jsonify({"status": "failed"})
        
if __name__ == '__main__':
	app.run(debug=True)
