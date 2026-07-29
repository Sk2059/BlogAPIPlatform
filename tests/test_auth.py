import pytest


@pytest.mark.asyncio
async def test_register_user(client):

    response = await client.post(
        "/auth/register",
        json={
            "email": "pytest_register@example.com",
            "username": "pytest_register",
            "password": "pytest#123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "pytest_register@example.com"
    assert data["username"] == "pytest_register"

    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):

    user = {
        "email": "duplicate@example.com",
        "username": "duplicate_user",
        "password": "pytest#123"
    }

    await client.post(
        "/auth/register",
        json=user
    )

    response = await client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "username": "another_user",
            "password": "pytest#123"
        }
    )

    assert response.status_code == 400