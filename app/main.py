from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME
)


@app.get("/")
async def root():
    return {
        "message": "Blog API Platform Running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }