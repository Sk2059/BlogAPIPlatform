import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from app.main import app
import uuid
import pytest

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
async def access_token(client):

    email = f"{uuid.uuid4().hex}@example.com"
    username = f"user_{uuid.uuid4().hex[:8]}"

    await client.post(
        "/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "pytest#123"
        }
    )

    response = await client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "pytest#123"
        }
    )

    return response.json()["access_token"]