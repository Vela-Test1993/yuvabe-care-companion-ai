from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from api_routes.chat_api import router as chat_router
from api_routes.knowledge_base_api import router as knowledge_base_router
from api_routes.chat_history_db_api import router as chat_history_router

description = (
    "Yuvabe Care Companion AI is designed to provide helpful and accurate "
    "responses to health-related queries. It offers insights from curated "
    "knowledge bases and maintains chat history for improved user experience."
)

app = FastAPI(
    title="Yuvabe Care Companion AI",
    description=description,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Cache-Control"],
)

@app.get("/", tags=["Root"], summary="Root Endpoint", response_model=dict)
def read_root():
    """Health check endpoint for confirming the API is active."""
    return {
        "message": "Yuvabe Care Companion AI is running successfully.",
        "timestamp": datetime.now().isoformat()
    }

# Register Routes
app.include_router(chat_router)
app.include_router(knowledge_base_router)
app.include_router(chat_history_router)
