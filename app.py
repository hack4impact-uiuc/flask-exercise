from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


def update_db():
    with open('mockdb/dummy_data.py', 'w')as f:
        f.writelines("initial_db_state = "+str(db.db_state))


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


@app.route("/users", methods=['GET'])
def all_users():
    data = db.get("users")
    if (request.args.get('team')):
        team = request.args.get('team')
        data = (list(filter(lambda x: x["team"] == team, data)))
    return create_response({"users": data})


@app.route("/users/<id>")
def user_by_id(id):
    data = db.getById("users", int(id))
    if (data == None):
        return create_response(status=404, message="The user does not exist yet")
    return create_response({"user": data})


@app.route("/users", methods=['POST'])
def create_new_user():
    user_data = request.get_json()
    required_fields = ["name", "age", "team"]
    if not all(field in user_data for field in required_fields):
        return create_response({"error": "Missing required fields"}, 400)
    data = db.create("users", user_data)
    update_db()
    return create_response(data)


@app.route("/users/<id>/", methods=['PUT'])
def update_user(id):
    user_data = request.get_json()
    required_fields = ["name", "age", "team"]
    if not all(field in user_data for field in required_fields):
        return create_response({"error": "Missing required fields"}, 400)
    data = db.updateById("users", int(id), user_data)
    if (data == None):
        return create_response(status=404, message="The user does not exist yet")
    update_db()
    return create_response(data)


@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    if (db.getById("users", int(id)) == None):
        return create_response(status=404, message="The user does not exist yet")
    db.deleteById("users", int(id))
    update_db()
    return create_response(message="User deleted successfully!")


"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
