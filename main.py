from fastapi import FastAPI
from app.v1.endpoints import user, order, endpoint
import uvicorn

app = FastAPI(debug=True, title="Online shop")

app.include_router(endpoint.router)
# app.include_router(user.router)
# app.include_router(order.router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port="8000")



