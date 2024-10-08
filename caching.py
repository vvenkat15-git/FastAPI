'''Caching is a technique used to store frequently accessed data or results in a temporary storage
    (cache) so that future requests can retrive this data faster
    without having to recompute or re-fetch it from the source.
    Caching imporves the performance and scalability of API's by reducing responce times and the
    load on the database or other extenal services
    '''

#How to implement caching in fastapi
'''In Fastapi to implement the caching we need to use various libraries and techniques.
    A Popular choice for caching in python applications AIOCACHE, which supports different types
    cache backends like REdis, Memcached, and in-memory caching.
    '''

#install the dependencies
'''pip install aiocache'''

'''user aiocache decoratos or methods to cache specific endpoints or expensive operations.'''


#example of Caching code

from fastapi import FastAPI
from aiocache import cached
import time

app = FastAPI()

#caching the responce for 10 seconds

@app.get("/cached-items/")
@cached(ttl=10)   #cache for 10 seconds
async def get_items():
    time.sleep(2)
    return {"items": ["item1", "item2", "item3"]}

#Explanation
'''
@cached(ttl=10): This decorator is used to cache the result of the get_items function for 10 seconds (ttl stands for "time-to-live"). During this period,
 any request to the /cached-items/ endpoint will return the cached result immediately, without re-executing the function.

time.sleep(2): This simulates a slow operation. Without caching, 
every request would take at least 2 seconds to complete. With caching, the first request takes 2 seconds, but subsequent requests within the 10-second cache window are instant.'''
