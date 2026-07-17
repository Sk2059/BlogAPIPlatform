from datetime import datetime , timedelta, timezone
from jose import jwt 
from app.core.config import settings

def create_access_token(subject:str) -> str:
    expire = datetime.now(
        timezone.utc
    )+timedelta(
        minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub":subject,
        "exp":expire,
        "type":"access"
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm= settings.ALGORITHM
    )

def create_refresh_token(subject:str) -> str:
    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload ={
        "sub":subject,
        "exp":expire,
        "type":"access"
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm= settings.ALGORITHM
    )