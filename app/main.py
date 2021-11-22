from fastapi import FastAPI
import uvicorn
import json


# Init
app = FastAPI(debug=True, title="Random phrase")

# Data
with open("books.json") as f:
    books = json.load(f)


# Route
@app.get('/api/v2/books')
async def get_books():
    return {"books": books}


@app.get('/')
async def get_main():
    return {"books": "12345"}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port="8000")



