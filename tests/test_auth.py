import pytest


@pytest.mark.asyncio
async def test_register(client):

    response = await client.post(
        "/auth/register",
        json={
            "email": "pytest_user@example.com",
            "username": "pytest_user",
            "password": "pytest#123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "pytest_user@example.com"

    assert data["username"] == "pytest_user"

    assert "id" in data