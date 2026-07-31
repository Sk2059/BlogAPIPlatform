import uuid

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.database import AsyncSessionLocal
from app.db.session import get_db  


async def override_get_db():
    async with AsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(
        app=app,
        raise_app_exceptions=True,
    )

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client

    await transport.aclose()


@pytest_asyncio.fixture
async def access_token(client: AsyncClient):
    email = f"{uuid.uuid4().hex}@example.com"
    username = f"user_{uuid.uuid4().hex[:8]}"

    register_response = await client.post(
        "/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "pytest#123",
        },
    )

    assert register_response.status_code == 201, register_response.text

    login_response = await client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "pytest#123",
        },
    )

    assert login_response.status_code == 200, login_response.text

    return login_response.json()["access_token"]