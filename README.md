# Flask Routes

This creates an application instance
__name__ is used to determine the root path of the application folder

```python
from flask import Flask
app = Flask(__name__)
```

Running the Server

```python
if __name__ == '__main__':
	app.run(debug=True)
```

App routes define the path to different pages in your application. This means that when you run python app.py, on http://127.0.0.1:5000/ it will run the function my_first_route that will print hello world. 
```python
@app.route('/')
def my_first_route():
	return "<h1> Hello World! </h1>"
```
You can have multiple routes. So for instance, the code below would run on http://127.0.0.1:5000/route/aria,
"aria" in this case is the parameter name, which can be anything you want. This is taken asn a input into the function my_second_route, and then the name is printed to the screen. 

```python
@app.route('/route/<name>')
def my_second_route(name):
     return name
```

**Problem 1: Write a route that takes a first name, last name, and graduating year in the route**


So, what are we using Flask for and why are routes useful. 

An API, or Application Programming Interface, is a set of subroutine definitions, protocols, and tools for building application software. It defines communication between various software components. 

Lets give an example. Let's say on the frontend you want to display all a list of names that are stored in your database. You are going to send a GET request that will be sent to one of these routes that you define in Flask. The function to handle the route will understand that you are trying to get some information, retrieve it from the database, and set in back to the frontend in a json format. 

```python
@app.route('/get_users', methods=['GET'])
def get_all_users():
    if request.method == 'GET':
    # Accesses the database and gets a list of names stored in the variable called data 
	# (ignore how you access the database for now, we'll come back to it)
	    return jsonify({'status': 'success', 'data':  ['aria', 'tim', 'varun', 'alex']})
    else:
        return jsonify({"status": "failed")
```

The GET request is part of a protocol called REST, which stands for Representational State Transfer. 

There are many types of requests, put the most important ones are: 
	GET: gets information from a database
	POST: adds information to a database
	PUT: modifies information in a database
	DELETE: deletes information in a database

From the nnb project, you can see an example of a get request that uses postgress database. Maps.query.all() goes into postgress, finds the table labeled Maps, and gets everything. The data is then put into a list and turned into a json object. If it fails, it will send the correct error message
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

Everything that I described above is what you're going to be working on in the Flask backend. This means figuring out how to design your database, and then define the API to make changes in your database. 

**Problem 2: Download Postman, go to the url for get_all_users, and set a GET request. If you make the wrong type of request, you will get an error message**

Setting up the database and defining it is alot of work, so we'll leave that for your tech leads to teach you :P 
For now, we're going to try actually using a public API to get more familair with it.

**Problem 3: Write an endpoint that will take an input, search for that term on wikipeida using the API, and then return back a list of titles of the top matches**