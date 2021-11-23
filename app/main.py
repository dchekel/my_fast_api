from fastapi import FastAPI
from typing import Optional
import uvicorn
import json


# Init
app = FastAPI(debug=True, title="Online shop")

# Data
with open("any_file.json") as f:
    books = json.load(f)


# Route
@app.get('/')
async def read_root():
    return {"Hello": "online shop with FastAPI"}


@app.get('/api/v2/books')
async def get_books():
    return {"books": books}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/users/{u_id}")
async def get_user(u_id: int):
    return {"id": u_id}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port="8000")



