# pytest automatically injects fixtures
# that are defined in conftest.py
# in this case, client is injected
from flask import json


def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["result"]["content"] == "hello world!"


def test_mirror(client):
    res = client.get("/mirror/Tim")
    assert res.status_code == 200
    assert res.json["result"]["name"] == "Tim"


def test_get_users(client):
    res = client.get("/users")
    assert res.status_code == 200
    res_users = res.json["result"]["users"]
    assert res_users[0]["name"] == "Aria"


def tests_get_users_with_team(client):
    res = client.get("/users?team=LWB")
    assert res.status_code == 200
    res_users = res.json["result"]["users"]
    assert res_users[1]["name"] == "Tim"


def test_get_user_id(client):
    res = client.get("/users/1")
    assert res.status_code == 200
    res_user = res.json["result"]["user"]
    assert res_user["name"] == "Aria"
    assert res_user["age"] == 19


def test_get_user_id_not_exist(client):
    res = client.get("/users/6")
    assert res.status_code == 404
    assert res.json["result"] == None
    assert res.json["message"] == "id:6 is not exist"
    assert res.json["success"] == False


def test_add_user(client):
    res = client.post(
        "/users",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"age": 20, "name": "Aria", "team": "LWB"}),
    )
    assert res.status_code == 201
    res_user = res.json["result"]["newUser"]
    assert res_user["name"] == "Aria"
    assert res_user["age"] == 20


def test_add_user_Missing_or_incorrect_data(client):
    res = client.post(
        "/users",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"name": "Aria", "team": "LWB"}),
    )
    assert res.status_code == 422
    assert res.json["result"] == None
    assert bool(res.json["message"])


def test_update_user_id(client):
    res = client.put(
        "users/1",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"age": 30}),
    )
    assert res.status_code == 200
    res_user = res.json["result"]["user"]
    assert res_user["age"] == 30
    assert res_user["name"] == "Aria"


def test_update_user_id_not_exist(client):
    res = client.put(
        "/users/6",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"age": 30}),
    )
    assert res.status_code == 404
    assert res.json["result"] == None
    assert res.json["message"] == "id:6 is not exist"
    assert res.json["success"] == False


def test_delete_user_id(client):
    res = client.delete("/users/4")
    assert res.status_code == 200
    assert res.json["success"] == True
    assert res.json["message"] == "The user with id:4 was deleted"


def test_delete_user_id_not_exist(client):
    res = client.delete("/users/10")
    assert res.status_code == 404
    assert res.json["result"] == None
    assert res.json["message"] == "id:10 is not exist"
    assert res.json["success"] == False
