# pytest automatically injects fixtures
# that are defined in conftest.py
# in this case, client is injected
import json


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
    assert len(res_users) == 4
    assert res_users[0]["name"] == "Aria"


def tests_get_users_with_team(client):
    res = client.get("/users?team=LWB")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 2
    assert res_users[1]["name"] == "Tim"


def test_get_user_id(client):
    res = client.get("/users/1")
    assert res.status_code == 200

    res_user = res.json["result"]["user"]
    assert res_user["name"] == "Aria"
    assert res_user["age"] == 19


def test_get_user_id_with_not_exist_id(client):
    res = client.get("/users/78")
    assert res.status_code == 404
    assert res.json["message"] == "user not found"


def test_add_new_user(client):
    res = client.post(
        "/users",
        data=json.dumps({"name": "mali", "age": 8, "team": "LWB"}),
        headers={"Content-Type": "application/json"},
    )
    assert res.status_code == 201
    res_user = res.json["result"]["newUser"][0]
    assert res_user["name"] == "mali"
    assert res_user["age"] == 8


def test_add_new_user_with_uncorrect_detailes(client):
    res = client.post(
        "/users",
        data=json.dumps({"age": 8, "team": "LWB"}),
        headers={"Content-Type": "application/json"},
    )
    assert res.status_code == 401
    assert res.json["message"] == "you have to send correct the:name"


def test_update_user(client):
    res = client.put(
        "/users/1",
        data=json.dumps({"name": "gili"}),
        headers={"Content-Type": "application/json"},
    )
    assert res.status_code == 201
    assert res.json["message"] == "successfully updated"


def test_update_user_with_not_exist_id(client):
    res = client.put(
        "/users/15",
        data=json.dumps({"name": "gili"}),
        headers={"Content-Type": "application/json"},
    )
    assert res.status_code == 404
    assert res.json["message"] == "the user id is not found"


def test_delete_user(client):
    res = client.delete(
        "/users/1",
        data=json.dumps({"name": "gili"}),
        headers={"Content-Type": "application/json"},
    )
    assert res.status_code == 201
    assert res.json["message"] == "successfully deleted"


def test_delete_user_with_not_exist_id(client):
    res = client.delete(
        "/users/89",
        data=json.dumps({"name": "gili"}),
        headers={"Content-Type": "application/json"},
    )
    assert res.status_code == 404
    assert res.json["message"] == "the user id is not found"
