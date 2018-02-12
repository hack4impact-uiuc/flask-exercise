from flask import Flask, jsonify, request

app = Flask(__name__)

def create_response(data={}, status=200, message=''):
    """
    Wraps response in a consistent format throughout the API
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response

    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself
    """
    response = {
        'success': 200 <= status < 300,
        'code': status,
        'message': message,
        'result': data
    }
    return jsonify(response), status

"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""

@app.route('/')
def my_first_route():
    return create_response(data='hello world!')

@app.route('/mirror/<name>')
def my_second_route(name):
    return create_response(name)

@app.route('/users', methods=['GET'])
def get_all_users():
    if request.method == 'GET':
        data = { 'users': ['aria', 'tim', 'varun', 'alex'] }
        return create_response(data)

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == '__main__':
    app.run(debug=True)
