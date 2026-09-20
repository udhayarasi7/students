from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.database import engine, Base
from app.api.v1 import students, chatbot

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API service for student database integrated with LangGraph AI Agent.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router, prefix="/api/v1")
app.include_router(chatbot.router, prefix="/api/v1")

# --- UI Route ---
@app.get("/", tags=["UI"])
def serve_ui():
    return FileResponse("index.html")