""" In FastAPI, routes are defined using python functions that are decorated with fastapi HTTP method decorators like
    "@app.get", "@app.post", "@app.put", "@app.delete",  and more
    these decorators specify the type of HTTP request the fucntion will respond to and the route(path) for that request."""

#Defining routes
"""Fast api provides a strightforward way to define routes by associating an http method with specific url path
    The routes handles(view functions) can be either synchronus or asychronuys
    """


#examples with different routes

#import the dependencies
from fastapi import FastAPI

app = FastAPI()

#define a GET route

@app.get("/")
def get_root():
    return {"message": "Welcome to Fastapi"}


#explantion
"""GET Route (/):
This route listens for GET requests at the root URL ("/").
It simply returns a message {"message": "Welcome to FastAPI"}."""

#get a specific route with path parameters
@app.get("/items/{item_id}")
def get_a_specific_item(item_id: int):
    return {"item_id": item_id, "message":"Item found"}

#explaintion
"""GET Route with Path Parameter (/items/{item_id}):
This route uses a path parameter (item_id), which is captured from the URL.
For example, a request to /items/10 will return: {"item_id": 10, "message": "Item found"}."""

#Define a post route
@app.post("/items")
def create_item(name: str, price:float):
    return {"name": name, "price": price}

"""POST Route (/items/):
This route listens for POST requests to create a new item.
It accepts name and price parameters and returns them in the response.
Example request
jsonbody we are sending
{
  "name": "Laptop",
  "price": 1200.00
}
json responce we are getting
{
  "name": "Laptop",
  "price": 1200.00
}
"""

#define a put route

@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, price: float):
    return {"item_id": item_id, "name": name, "price": price}

"""PUT Route (/items/{item_id}):
This route listens for PUT requests to update an existing item.
It takes an item_id from the URL and name, price from the body.
Example: PUT /items/1 with name="New Laptop", price=1000.00.
Response:
{
  "item_id": 1,
  "name": "New Laptop",
  "price": 1000.00
}
"""
#Define a delete route
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"item with id {item_id} has been deleted"}

"""DELETE Route (/items/{item_id}):
This route listens for DELETE requests to remove an item with the given item_id.
Example: DELETE /items/1 would return:"""

"""Route Parameters:
"Path parameters": Captured directly from the URL, such as /items/{item_id}.
"Query parameters": Can be added as part of the URL query string, for example /items/?name=laptop&price=1000.00 in GET requests.
"Request body": Used in POST or PUT requests to send more complex data like JSON or form data."""

