import pytest


@pytest.mark.asyncio
async def test_create_post(client, access_token):

    response = await client.post(
        "/posts",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "title": "My First Blog",
            "content": "FastAPI is amazing!"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "My First Blog"
    assert data["content"] == "FastAPI is amazing!"
    assert "id" in data