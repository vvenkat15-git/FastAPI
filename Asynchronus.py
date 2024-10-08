""" FastAPI is designed to handle asynchronous programming by natively supporting
    asynchronous I/O operations through Python’s "async" and "await" keywords.
    This is especially important in web applications because it allows
    for non-blocking execution of tasks that might otherwise cause delays,
    such as handling multiple requests,
    I/O operations (like database calls or file I/O), or network requests."""

"""Importance of asychronus programming
    1. efficiency
    2. Performace
    3. Scalibility """

#Can you explain asynchronous vs. synchronous execution in Python?
'''Answer: In synchronous execution, tasks are executed one after the other, 
   potentially causing bottlenecks. Asynchronous execution allows tasks to be 
   run concurrently, especially useful for I/O-bound tasks like database queries. 
   In FastAPI, async endpoints use async and await keywords to handle 
   multiple requests concurrently.
'''

#example of fastapi asychronus programming

#import items
from fastapi import FastAPI
import asyncio
import time

#defining the app
app = FastAPI()

#Asychronus Route
@app.get("/async")
async def async_route():
    await asyncio.sleep(2)  # Simulate a long-running operation
    return {"message": "This is an asychronus end point"}

#Synchronus Route
@app.get("/sync")
def sync_route():
    time.sleep(2)
    return {"message": "This is synchronus endpoint!"}

""" explanation
    "Asynchronus Route"
    1. async def async_route(): This defines an asynchronous function in Python.
    2. await asyncio.sleep(2): Instead of blocking the server for 2 seconds,
       the server can handle other requests during this time.

    "Synchronus Route:
    1. time.sleep(2) blocks the execution for 2 seconds, preventing the server from
       responding to other requests during that time.
    """

""" How fastapi handles the asychronus programming
    When the asynchronous function "async_route" is called,
    FastAPI schedules it for execution and continues handling other tasks, making it more responsive.

    The synchronous function "sync_route" will block the server thread until the sleep finishes,
    making it less efficient for high-concurrency scenarios.
    """

"""In large-scale applications, asynchronous programming in FastAPI allows handling of many I/O-bound tasks
 (like reading from databases or external APIs) more efficiently,
   making the application much more performant and scalable."""
