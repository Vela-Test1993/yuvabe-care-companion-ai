# from fastapi import FastAPI
# from routes import knowledge_base_api
# from fastapi.middleware.cors import CORSMiddleware
# from utils import logger 

# # Initialize FastAPI app
# app = FastAPI(
#     title="HealthCare VectorDB API",
#     description="API for managing Pinecone VectorDB operations for healthcare data.",
#     version="1.0.0"
# )

# # Logger setup
# logger = logger.get_logger()

# # CORS Middleware (for better cross-origin request handling)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust for security if needed
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include API routes
# app.include_router(knowledge_base_api.router, prefix="/knowledge-base", tags=['Knowledge Base Operations'])


# # Health Check Endpoint
# @app.get("/health", tags=["Health Check"])
# async def health_check():
#     return {"status": "API is healthy and running."}

from fastapi import FastAPI
from api_routes.chat_api import router as chat_router
from api_routes.knowledge_base_api import router as knowledge_base_router

app = FastAPI(
    title="Yuvabe Care Companion AI",
    description="A chatbot for health-related queries",
    version="1.0.0"
)

# Register Routes
app.include_router(chat_router)
app.include_router(knowledge_base_router)
