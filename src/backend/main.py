from fastapi import FastAPI
from routes.chat_api import router as chat_api

app = FastAPI()

app.include_router(chat_api, prefix="/chat", tags=["chat"])