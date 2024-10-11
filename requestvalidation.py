"""Fast api handles the request validation automatically using the "pydantic models.
    it validates both the request body, and parameters(path, query) etc
    Before passing them to our route handler, ensure that the incoming data meets our
    specified constraints """

#Key features of Request Validation
"""  Automatic
     Error Handling
     Decalrative
     Type safety """

#Basic Query Parmeter Validation
"""Fastapi validates the query parameters based on the conditions"""

#code
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
def read_items(limit: int = Query(10, gt=0, le=100), q:str = None):
    return {"limit": limit, "q":q}

#validation rules

""" "Limit": The query fucntion validates the limit parameter is an integer between 1 and 100(gt = 0 , le = 100)
     if the limit is outside this range or not an intger fastapi valiation error"""

#example request
# /items/?limit=5&q=laptop

#example request responce
'''{"limit":5,
    "q":"laptop"}'''

#example invalid request
# /items/?limit=0  it fails validation since limite must be greater than 0

"""________________________________________________________________________________________________________________"""


#Request Body validation with pydantic models

#we can user pydantic models to validate the request body

#code example

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

#Define a Pydantic model for request validation
class Item(BaseModel):
    name :str
    price: float = Field(..., gt=0)
    description: str = Field(None, max_length=300)


@app.post("/items/")
def create_item(item:Item):
    return {"item": item}

#validation rules
"""name: Must be a string (required field).
price: Must be a positive float (gt=0 ensures the price is greater than 0).
description: Optional field (None by default), but if provided, it must not exceed 300 characters (max_length=300)."""

#example request body valid

'''{
  "name": "Laptop",
  "price": 1200.00,
  "description": "A high-end gaming laptop"
}'''

#example responce

'''{
  "item": {
    "name": "Laptop",
    "price": 1200.00,
    "description": "A high-end gaming laptop"
  }
}'''

#example on invalid request body 

'''{
  "name": "Laptop",
  "price": -1200.00
}
'''

#error responce
'''{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt",
      "ctx": {"limit_value": 0}
    }
  ]
}'''

#in the above case fastapi checks the price is a positive integer, if it is negative
#fastapi automatically returns an error message


'''_________________________________________________________________________________________________'''

#PATH PARAMETER VALIDATION

#we can validate path parameters by setting types and constrains on them.

#example code

from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/item/{item_id}")
def read_item(item_id: int = Path(..., gt=0)):
    return {"item_id":item_id}

'''Validtiaon rules
    "item_id": Must be a positive integer (gt=0 ensures that the item_id is greater than 0).'''

#example Request
#/items/10

#example responce

'''{
  "item_id": 10
    }
'''
#invalid request 
#/items/-5 fails value shoud be greater than 0

#error responce
'''{
  "detail": [
    {
      "loc": ["path", "item_id"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt",
      "ctx": {"limit_value": 0}
    }
  ]
}
'''

#why request validation is important:
#1, security, 2, robustness, 3, productivity

#by using fastapi pydantic models, and validation mechanisms we can build
#secure and well structured api's that prevent invalid data from being processed.
