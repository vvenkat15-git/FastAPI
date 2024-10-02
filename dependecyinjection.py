"""Dependency Injection in fastapi is a powerful feature that allows you to
    manange the dependencies(like database connections, authentication services, )
    and configurations, eetc,) into our routes or functions in a structures and reusable way """

"""With DI we can separate concerns in our applicatio, making our code 
    mode modular, maintable and testable. Fastapi dependecy injection
    system is also asychronus, allows us to decalre dependencies in 
    non-blocking way when necessary"""

"""Key Concepts of Dependency Injection in FastAPI:
"Reusable": Dependencies can be defined once and reused across multiple routes.
"Declarative": Dependencies are declared using Python's type annotations, and FastAPI handles their injection automatically.
"Modular": Dependencies can be composed or layered, i.e., one dependency can use another dependency.
"Asynchronous": Dependencies can be async functions that use await for I/O operations, which ensures efficiency."""


#example of Dependency Injection in FastAPI

from fastapi import FastAPI, Depends, HTTPException

app =FastAPI()

#lets create some fake user database

fake_user_db = {
        "alice": {"username":"alice",
                  "fullname": "Alice Wounderland"},
        "bob": {"username":"bob",
                "fullname":"Bob Builder"}
}

#Define a dependency to get the current user

def get_current_user(username:str):
    user = fake_user_db(username)
    if user is None:
        raise HTTPException(status_code = 404, detail = "user not found")
    return user

#Define a route that depends on the get_current_user dependency

@app.get("/users/me")
def read_current_user(username:str, current_user: dict = Depends(get_current_user)):
    return current_user

#Another route using the same dependency

@app.get("/users/{username}")
def read_user(username: str, current_user: dict = Depends(get_current_user)):
    return{"message": f"hello {current_user["full_name"]}, welcome back"}


#explanation

"""The "get_current_user" Dependency:
"get_current_user" is a function that takes a username and checks if the user exists in the fake_users_db.
If the user is found, it returns the user dictionary; otherwise, it raises an HTTP 404 exception.

Injecting the Dependency using Depends:
In the routes "read_current_user" and "read_user", we declare a dependency on "get_current_user"
 by passing Depends(get_current_user) to the current_user parameter.
FastAPI will automatically call the get_current_user function, pass the required arguments (in this case, username),
 and inject the returned value (current_user) into the route handler.

Handling User Authentication:
When a request is made to /users/me?username=alice, FastAPI automatically injects the user object returned by
get_current_user into the current_user argument of the route.
If the user does not exist, the dependency raises an HTTP 404 exception, and the route handler is not executed."""

#why to user dependecy injection 1, codereuse, 2, modularity, 3, Testability
