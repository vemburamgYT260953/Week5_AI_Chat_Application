
from fastapi import FastAPI

from app.routes import router
from app.storage import initialize_csv
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI(
    title="AI Chat Application",
    description="CSV-based LLM Chat Backend",
    version="1.0.0"
    
)

initialize_csv()

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "AI Chat Application Backend Running Successfully"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
