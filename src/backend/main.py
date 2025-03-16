from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_routes.chat_api import router as chat_router
# from api_routes.knowledge_base_api import router as knowledge_base_router
# from api_routes.chat_history_db_api import router as chat_history_router

app = FastAPI(
    title="Yuvabe Care Companion AI",
    description="A chatbot for health-related queries"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Cache-Control"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Hello World"}

# Register Routes
app.include_router(chat_router)
# app.include_router(knowledge_base_router)
# app.include_router(chat_history_router)

# Health Check Endpoint
@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "API is healthy and running."}
