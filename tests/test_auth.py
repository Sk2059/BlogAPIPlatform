import pytest
import uuid


def unique_email():
    return f"{uuid.uuid4().hex}@example.com"


def unique_username():
    return f"user_{uuid.uuid4().hex[:8]}"


@pytest.mark.asyncio
async def test_register_user(client):

    email = unique_email()
    username = unique_username()

    response = await client.post(
        "/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "pytest#123"
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["username"] == username
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):

    email = unique_email()

    await client.post(
        "/auth/register",
        json={
            "email": email,
            "username": unique_username(),
            "password": "pytest#123"
        }
    )

    response = await client.post(
        "/auth/register",
        json={
            "email": email,
            "username": unique_username(),
            "password": "pytest#123"
        }
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_register_duplicate_username(client):

    username = unique_username()

    await client.post(
        "/auth/register",
        json={
            "email": unique_email(),
            "username": username,
            "password": "pytest#123"
        }
    )

    response = await client.post(
        "/auth/register",
        json={
            "email": unique_email(),
            "username": username,
            "password": "pytest#123"
        }
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client):

    email = unique_email()
    username = unique_username()

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

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client):

    email = unique_email()
    username = unique_username()

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
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_unknown_email(client):

    response = await client.post(
        "/auth/login",
        json={
            "email": unique_email(),
            "password": "pytest#123"
        }
    )

    assert response.status_code == 401