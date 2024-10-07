#Authentication
'''This is the process of verifying who a user is. In FastAPI, 
   authentication involves confirming the identity of a user, 
   typically through login credentials such as a username and password, 
   or tokens like JWT (JSON Web Token).'''

#Authorization
'''Once a user is authenticated, authorization determines what the user is allowed to do.
   This checks the user's permissions or roles to ensure they have access to a particular 
   resource or action.'''

'''In Fastapi we can implement authetication and authorization using dependencies like
    OAuth2, or JWT tokens, 
    Fastapi provides builtinsupport for various security protocols in this way.'''


#Exaple of Implementing User Authentication and Authrization using JWT

# 1. JWT Token based-Authentication
'it is commonly used in authetication to ensure that users are authenticated and authorized'

#code:

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional


#Secret key for encoding JWT Tokens
SECRET_KEY = "our_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#FAKE DATABASE FOR CHECKING

fake_users_db = {
    "johndoe": {
        "username":"johndoe",
        "full_name":"John Doe",
        "email":"johndoe@example.com",
        "hashed_password":"fakehashedpassword",
        "disabled":False,
    }
}

#Pydantic Model for token
class Token(BaseModel):
    access_token = str
    token_type = str


#Pydantic model for Token Data
class TokenData(BaseModel):
    username: Optional[str] = None


#Pydantic model for user

class User(BaseModel):
    username : str
    email : Optional[str] = None
    full_name : Optional[str] = None
    disabled : Optional[str]= None

#Pydantic model for userinDB

class UserInDB(User):
    hashed_password : str

#Defining Oauth2 Scheme

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

app = FastAPI()


#utility function to verify password (simulating password hashing)

def verifypassword(plain_password, hased_password):
    return plain_password == hased_password # simplified for demostration

#Function to get user from the fake database

def get_user(db, username, str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None


#Function to authenticate user
def authenticate_user(fake_db, username:str, password:str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verifypassword(password, user.hashed_password):
        return False
    return user

'''Authentication:

   "authenticate_user": This function checks if the provided username and password match the stored
     credentials (simulated here with a fake database).'''


#Function to create JWT TOKEN

def create_access_token(data: dict, expires_delta: Optional[timedelta]= None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

'''1. JWT Token Creation:

    "create_access_token": Generates a JWT token with user data (sub stands for "subject", 
    which in this case is the username) and an expiration time. It uses the HS256 algorithm
    for signing the token.'''


#Dependency to get the current user form the token

async def get_current_user(token: str =Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate the credentials",
        headers = {"WWW-AUTHENTICATE": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username :str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username = username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username= token_data.username)
    if user is None:
        raise credentials_exception
    return user

#dependcy to verify if the current user is active

async def get_current_active_user(current_user: User =  Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail = "Inactive user")
    return current_user

'''Authorization:

get_current_user: This function decodes the JWT token from the
                  request and retrieves the user associated with it.
get_current_active_user: Checks if the user is active (i.e., not disabled)
                         and raises an error if not.'''


#route to login in get token

@app.post("/token", responce_model = Token)
async def login_for_access_token(fromdata, OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, from_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details = "Incorret username or password",
            headers = {"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sun":user.username}, expires_delta=access_token_expires   
    )
    return {"access_token": access_token, "token_type":"bearer"}

'''Login Route (/token): This route accepts a username and password
   (via OAuth2PasswordRequestForm) and returns a JWT token if the credentials are valid'''

#protected route that requires authentication

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

#protected route that requires specific authorization(acitve user only)

@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return {"item": "You can view your items", "user":current_user.username}

'''Protected Routes:

/users/me: A protected route that returns the current authenticated user’s information.
/users/me/items: A protected route that requires the user to be active (authorized)
                 before accessing it.''' 

"how it workds"

'''Login Process:
The user sends a POST request to /token with their username and password.
If authenticated, the server responds with a JWT access token.'''

'''Accessing Protected Routes:
The user can then send the JWT token as a Bearer token in the Authorization header when making requests to protected endpoints.
FastAPI validates the token, retrieves the user data from it, and checks the user's authorization (active status in this example).'''


'''Error Handling:
   If a user tries to access a protected route without a valid token or with insufficient permissions, FastAPI will return an error (e.g., 401 Unauthorized or 400 Bad Request).'''

'''
Summary:
Authentication: Verify the user's identity (using JWT tokens in this case).
Authorization: Ensure the user has the correct permissions to access certain resources (e.g., checking if the user is active).
JWT: A secure, standard way to handle token-based authentication and authorization in FastAPI.
'''




 

        








