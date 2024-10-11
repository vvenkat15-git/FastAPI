'''In Fastapi- Cross-Origin Resource Sharing is handled using the "CORSMiddleware".
   CORS is security feature implemented by browsers that restricts web applications
   running at one origin
   "example"
   (http://example.com) from making requests to a different origin (http://api.example.com).
   If our fastapi is going to be accessed from a different domain, we need to enable CORS to allow the Cross origin requests
   '''

#Steps to Handle the CORS in FastAPI

#step1. Install the starlette: 
'''Fastapi users starlette internally, which includes the CORSMiddleware for hanlding CORS
'''
#step2 Eanble the CorsMiddleware in Fastapi
''' We need you add CORSMiddleware to our fastapi applicaiton and configure the allowed origins
    and methods and headers.
    '''
#code to Enableing CORS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#Define the list of allowed origins(domains)

origins = [
        "http://localhost",
        "http://localhost:8000",
        "http://example.com", #Example of another allowed origin
        ]

#Add CORS middleware to the FastAPI app

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,  # Allow cookies and other credentials
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allow specific HTTP methods
    allow_headers=["*"],  # Allow all headers
)

#get call
@app.get("/items/")
async def read_items():
    return [{"item": "item1"}, {"item":"item2"}]

#Explanation of the Parameters in CORSMiddleware:
'''allow_origins: A list of allowed origins (domains). You can specify which domains can access your API. If you want to allow any domain, you can set allow_origins=["*"], but be careful as this opens the API to all domains.
   allow_credentials: If set to True, allows cookies and other credentials such as authorization headers to be included in cross-origin requests.
   allow_methods: A list of allowed HTTP methods for CORS (e.g., GET, POST, PUT, DELETE, etc.). You can restrict specific HTTP methods that can be used from other origins.
   allow_headers: Specifies which headers can be included in cross-origin requests. You can allow all headers by setting allow_headers=["*"].
'''

#example of ALLOW all ORIGINS

'''If you want to allow all origins to access your API (not recommended in production unless necessary), you can set allow_origins=["*"]:'''

#code
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
'''

# Summery

'''CORS: CORS is necessary to allow cross-origin requests from other domains.
   CORSMiddleware: FastAPI handles CORS using CORSMiddleware, which is part of starlette.
   Configuration: You configure CORS by specifying allowed origins, methods, headers, and credentials.'''
