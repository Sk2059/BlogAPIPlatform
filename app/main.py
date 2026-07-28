from fastapi import FastAPI
from app.core.config import settings
from app.api.post import router as post_router
from app.api import comment
from app.api import like
from app.api.v1.auth import router as auth_router
from app.api.user import router as user_router
app = FastAPI(
    title=settings.APP_NAME
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment.router)
app.include_router(like.router)

@app.get("/")
async def root():
    return {
        "message": "Blog API Platform Running"
    }


