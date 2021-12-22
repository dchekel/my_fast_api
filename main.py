from fastapi import FastAPI
from app.v1.endpoints import user, order, endpoint
import uvicorn

tags_metadata = [
    {"name": "Get Methods", "description": "Yes, take it all."},
    {"name": "Post Methods", "description": "Keep doing this"},
    {"name": "Delete Methods", "description": "KILL 'EM ALL"},
    {"name": "Put Methods", "description": "It's worth a try"},
]
app = FastAPI(debug=True, title="Online shop", openapi_tags=tags_metadata)

app.include_router(endpoint.router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port="8000")


#
# простого процесса логирования/добавления товара в корзину/ удаления товара/покупки
#
# и еще добавить роль админ который может добавлять категории, добавлять товар
#
# т.е. можно сделать две роли пользователь/админ
