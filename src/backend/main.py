from fastapi import FastAPI
from routes.chat_api import router

app = FastAPI()

app.include_router(router, prefix="/chat", tags=["chat"])