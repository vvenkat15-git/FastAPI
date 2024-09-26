from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional



#define the secret key, algorithm, Access_token_expire_minutes.

SECRET_KEY = "2a8649bda71332e8f8c580b7fcadb4c5c1a284ee852817fe6a5e18f590fc57df"
ALGORITHM = "HS256"
ACCES_TOKEN_EXPIRE_MINUTES = 30

#secret key is using as a part of encryption and hasih the password

db = {
    "venkat":{
        "username":"venkat",
        "full_name":"venkat Vanukuru",
        "email": "venkat#gmail.com",
        "password": "",
        "disabled": False

    }
}

class Token(BaseModel):
    access_token : str
    token_type :str

class Tokendata(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username : str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled : Optional[bool] = None



class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl = "token")




app = FastAPI()


#hashing password
def verify_password(plain_password, hashed_password):
    return pwd_context(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)
    
def auttheticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_accestoken(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 15)

    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM )
    return encode_jwt

#Lets start looking at authentication and authorization


async def get_current_user(token:str = Depends(oauth_2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "could not validate credentials", headers ={"WWW-Authenticate":"Bearer"} )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm = [ALGORITHM])
        username : str = payload.get("sub")
        if username is None:
           raise credential_exception
        
        token_data = Tokendata(username=username)
    except JWTError:
        raise credential_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception

    return user


async def  get_current_active_user(current_user: UserInDB =Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code= 400, detial= "Inactive user")
    
    return current_user



@app.post("/token", response_model=Token)
async def login_for_access_token(form_data:OAuth2PasswordRequestForm = Depends()):
    user = auttheticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "incorrent user name or password", headers ={"WWW-Authenticate":"Bearer"})

    access_token_expires = timedelta(minutes = ACCES_TOKEN_EXPIRE_MINUTES)
    access_token = create_accestoken(data={"sub":user.username}, expires_delta = access_token_expires)
    return {"access_token":access_token,"token_type" :"bearer"}


@app.get("/user/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/user/me/items")
async def read_own_item(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner":current_user}]


# pwd = get_password_hash("venkat123")
# print(pwd)
