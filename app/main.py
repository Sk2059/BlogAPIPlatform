from fastapi import FastAPI
from app.core.config import settings

from app.api.v1.auth import router as auth_router
app = FastAPI(
    title=settings.APP_NAME
)

app.include_router(
    auth_router
)

@app.get("/")
async def root():
    return {
        "message": "Blog API Platform Running"
    }


