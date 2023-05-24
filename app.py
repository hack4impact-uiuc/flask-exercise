from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db
from mockdb.dummy_data import initial_db_state

db_state = initial_db_state

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


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    return create_response({"name": name})


@app.route("/users/<id>")
def get_users_by_id(id):
    if db.getById("users", int(id)):
        return create_response({"user": db.getById("users", int(id))})
    return create_response({}, 404, "user not found")


@app.route("/users")
def get_users_in_team():
    if request.args.get("team"):
        return create_response(
            {
                "users": list(
                    filter(
                        lambda x: x["team"] == request.args.get("team"), db.get("users")
                    )
                )
            }
        )
    return create_response({"users": db.get("users")})


@app.route("/users", methods=["POST"])
def add_new_user():
    user = request.get_json()
    message = "you have to send correct the:"
    if "name" in user and "age" in user and "team" in user:
        return create_response({"newUser": [db.create("users", user)]}, 201)
    if "name" not in user:
        message += "name"
    if "age" not in user:
        message += "age"
    if "team" not in user:
        message += "team"
    return create_response({}, 401, message)


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    details = request.get_json()
    if db.updateById("users", int(id), details) != None:
        return create_response({}, 201, "successfully updated")
    return create_response({}, 404, "the user id is not found")


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    if db.getById("users", int(id)) == None:
        return create_response({}, 404, "the user id is not found")
    db.deleteById("users", int(id))
    return create_response({}, 201, "successfully deleted")


# TODO: Implement the rest of the API here!

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""

if __name__ == "__main__":
    app.run(debug=True)
