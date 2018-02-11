# Flask Take Home Exercises

## Setup
You must have python3.6 and pip installed. To do this, check out the wiki and the page named "Mac Setup".
First, clone this repository and go into it:
```
$ git clone https://github.com/hack4impact-uiuc/FlaskTutorial.git
$ cd FlaskTutorial
```
Then, install `virtualenv` and go into it. This allows you to have a virtual environment that for your specific application. 
```
$ pip3 install virtualenv
$ virtualenv -p python3 venv
$ source venv/bin/activate
```
You will then have a (venv) before the $, meaning that you are now in your virtual environment. Then, install the Flask.
```
(venv)$ pip3 install Flask
(venv)$ pip3 install requests
```
You must be in this virtual environment to start this server. To start the server run:
```
(venv)$ python app.py
```
To stop the server, do `Control-C`. Also, to exit your virtual environment, which is named `venv` run:
```
(venv)$ deactivate venv 
```

## Exercises
This creates an application instance
__name__ is used to determine the root path of the application folder

```python
from flask import Flask
app = Flask(__name__)
```

Running the Server:

```python
if __name__ == '__main__':
	app.run(debug=True)
```

App routes define the path to different pages in your application. This means that when you run python app.py, on http://127.0.0.1:5000/ it will run the function `my_first_route` that will print hello world. 
```python
@app.route('/')
def my_first_route():
	return "<h1> Hello World! </h1>"
```
You can have multiple routes. So for instance, the code below would run on http://127.0.0.1:5000/route/aria,
"aria" in this case is the parameter name, which can be anything you want. This is taken as an a input into the function my_second_route, and then the name is printed to the screen. 

```python
@app.route('/route/<name>')
def my_second_route(name):
     return name
```

**Problem 1**
**Write a route that takes a first name, last name, and graduating year in the route. If this route is hit, wit print out the line `<firstname> <lastname> will graduate in <graduating_year>`**


So, what are we using Flask for and why are routes useful ... to build an API.

An API, or Application Programming Interface, is a set of subroutine definitions, protocols, and tools for building application software. It defines communication between various software components. 

Lets give an example. Let's say on the frontend you want to display all a list of names that are stored in your database. You are going to send a GET request that will be sent to one of these routes that you define in Flask. The function to handle the route will understand that you are trying to get some information, retrieve it from the database, and set in back to the frontend in a json format. 


The `GET` request is part of a protocol called REST, which stands for Representational State Transfer. 

There are many types of requests, put the most important ones are: 

`GET`: gets information from a database

`POST`: adds information to a database

`PUT`: modifies information in a database

`DELETE`: deletes information in a database

From the nnb project from last semester, you can see an example of a get request that uses postgress database. Maps.query.all() goes into postgress, finds the table labeled `Maps`, and gets everything. The data is then put into a list and turned into a json object. If it fails, it will send the correct error message
```python
#Gets all maps
@app.route('/maps', methods=['GET'])
def getallyears():
    if request.method == 'GET':
        try:
            print(len(Maps.query.all()))
            return jsonify({'status': 'success', 'data': serializeList((Maps.query.all()))})
        except Exception as ex:
            raise InvalidUsage('Error: ' + str(ex), status_code=404)
    else:
        return jsonify({"status": "failed", "message": "Endpoint, /years, needs a GET request"})
```

Here's a POST request example from the same project: 
```python
#Add a map
@app.route('/maps', methods=['POST'])
# @login_required
def addmapforyear():
    if request.method == 'POST':
        try:
            json_dict = json.loads(request.data)
            result = Maps(
                image_url = json_dict['image_url'],
                year = (int)(json_dict['year'])
            )
            db.session.add(result)
            db.session.commit()
            return jsonify({"status": "success", "message": "successfully added maps and year"})
        except Exception as ex:
            raise InvalidUsage('Error: ' + str(ex), status_code=404)
    else:
        return jsonify({"status": "failed", "message": "Endpoint, /maps, needs a GET or POST request"})
```

Everything that I described above is what you're going to be working on in the Flask backend. This means figuring out how to design your database, and then define the API to make changes in your database. 



**Problem 2:**

**So instead of making you guys actually use a database, simply make an array called *users* thats global in your app.py file. Each element in the array is a user with a id, name, and age**

For example 
```json

   users = [
       {
            "id": 1,
            "name": "Aria", 
            "age": 19
       }, 
        {
            "id": 2,
            "name": "Tim", 
            "age": 20
        }, 
        {
            "id": 3,
            "name": "Varun", 
            "age": 23
        }, 
        {
            "id": 4,
            "name": "Alex", 
            "age": 24
        } 
   ] 
```

**Then create a route for `/get_all_users` that will receive a GET request and return the list of all current users in a json format. It will return an error message for everything other than a GET request.**

**Next create a route called `/add_user` that will receieve a POST request. Inside the request data there will be a user with an id, name, and age. The function will take the request data and add a new user to the globale list of users. Also, add appropriate success/error responses in a json format.**

**Next create a route called `/modify_user` that will receieve a PUT request. In the request data have an id so they know which user is being modified, and then have a new name or age for the user. In the function, edit the user with that id in the global list of users. Also, add appropriate success/error responses in a json format.**

**Next create a route called `/delete_user` that will receieve a DELETE request and a name. The request data will have an id,and then that user is deleted from teh global array. Also, add appropriate sucess/error responses in a json format.**

**To test everything, download postman and make requests**

Setting up the database and defining it is alot of work, so we'll leave that for your tech leads to teach you. Also, for the course of this intro project, we're doing everything in app.py. **In your projects though, you are going to organize the endpoints into different files, have a folder to define the models, and other files for the database connection. **


## Message Shreyas for help but please use the channel #backend :)
