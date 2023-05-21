from typing import Tuple
import json
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
def write_data():
     new_data = json.dumps({"users" :db.get("users") })
     with open("mockdb/dummy_data.py" ,'w') as f:
          f.write( "initial_db_state = " + new_data )
    
@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

# TODO: Implement the rest of the API here!
@app.route("/users")
def get_users():
     data = db.get('users')
     team = request.args.get('team')
     if team == None:
        return create_response({"users":data}) 
     data_team = (list(filter(lambda x:x["team"]==team,data)))
     return create_response({"users":data_team}) 

@app.route("/users/<id>")
def get_users_by_id(id):
     data = db.getById("users",int(id))
     if data == None:
         return create_response({} , 404 , "User does not exist" )
     return create_response({"user":data})    

@app.route("/users", methods=['POST'])
def create_user():
        data = request.get_json()
        required_fildes = ["name","age","team"]
        if not all(filed in data for filed in required_fildes):
            return create_response({"None":None} , 422 ,"Missing data The object should contain: ID, name and team" )
        new_user={
           "name":data["name"], "age": data["age"], "team": data["team"]
         }
        res = db.create("users",new_user)
        write_data()
        return create_response({"users":res} , 201 ) 
           

@app.route("/users/<id>" , methods=['PUT'] )
def update_users(id):
     data = request.get_json()
     update_user = db.updateById("users", int(id) , data)
     if update_user == None:
        return create_response({"users":data} ,404 ,"" ) 
     write_data()
     return create_response({"users":update_user})
     

@app.route("/users/<id>" , methods=['DELETE'] )
def delete_user(id):
     data = db.getById("users",int(id))
     if data == None:
         return create_response({} , 404 , "User does not exist" )
     db.deleteById("users", int(id) )
     write_data()
     return create_response({} , 200 ,'')
             
"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
