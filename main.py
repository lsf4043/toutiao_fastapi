from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import news, user, favorite, history

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(news.router)
app.include_router(user.router)
app.include_router(favorite.router)
app.include_router(history.router)
