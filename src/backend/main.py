from fastapi import FastAPI
from backend.routes import chat_api

app = FastAPI()

app.include_router(chat_api.router, prefix="/chat", tags=["chat"])