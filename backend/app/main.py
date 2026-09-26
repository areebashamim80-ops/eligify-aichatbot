from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.auth import router as auth_router
from backend.app.api.chatbot import router as chatbot_router
from backend.app.api.schemes import router as schemes_router


app = FastAPI(
    title="Eligify API",
    description="AI-Driven Scheme Matching for Marginalized Entrepreneurs",
    version="1.0.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Authentication routes
app.include_router(auth_router)


# Eligify AI routes
app.include_router(chatbot_router)


# Government Schemes routes
app.include_router(schemes_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Eligify API",
        "status": "running",
        "ai": "enabled"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }