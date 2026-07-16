"""
main.py

FastAPI backend for the Network Troubleshooting Chatbot.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.rag_pipeline import ask_network_question


# ------------------------------------------
# Create FastAPI app
# ------------------------------------------

app = FastAPI(
    title="Network Troubleshooting Chatbot",
    version="1.0"
)

# ------------------------------------------
# Enable CORS
# ------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------
# Request Model
# ------------------------------------------

class ChatRequest(BaseModel):
    message: str


# ------------------------------------------
# Response Model
# ------------------------------------------

class ChatResponse(BaseModel):
    response: str


# ------------------------------------------
# Root Endpoint
# ------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Network Troubleshooting Chatbot API is running."
    }


# ------------------------------------------
# Chat Endpoint
# ------------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = ask_network_question(request.message)
    return ChatResponse(response=answer)