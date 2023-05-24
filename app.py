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
    data = {"name": name}
    return create_response(data)


@app.get("/users")
def getAllUsers():
    team = request.args.get("team")
    if team:
        return create_response(
            {"users": list(filter(lambda x: x["team"] == team, db.get("users")))}
        )
    return create_response({"users": db.get("users")})


@app.get("/users/<int:id>")
def getUserById(id):
    data = {"user": db.getById("users", id)}
    if data["user"]:
        return create_response(data)
    return create_response(None, 404, "id:{id} is not exist".format(id=id))


@app.post("/users")
def addUser():
    data = request.get_json()
    state = list(filter(lambda x: x not in data, ["name", "team", "age"]))
    if not bool(state):
        state = list(
            filter(
                lambda x: x in ["name", "team", "age"] and bool(data[x]) == False, data
            )
        )
        if not bool(state):
            req = {"newUser": db.create("users", request.get_json())}
            db.updateUsersData()
            return create_response(req, 201)
    return create_response(
        None,
        422,
        "Name, age and team must be entered and the following data was not entered:{state}".format(
            state=state
        ),
    )


@app.put("/users/<int:id>")
def updateUser(id):
    data = request.get_json()
    req = {"user": db.updateById("users", id, data)}
    if req["user"]:
        db.updateUsersData()
        return create_response(req)
    return create_response(None, 404, "id:{id} is not exist".format(id=id))


@app.delete("/users/<int:id>")
def deleteUser(id):
    if db.getById("users", id):
        data = {"users": db.deleteById("users", id)}
        db.updateUsersData()
        return create_response(
            None, 200, "The user with id:{id} was deleted".format(id=id)
        )
    return create_response(None, 404, "id:{id} is not exist".format(id=id))


# TODO: Implement the rest of the API here!
"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
