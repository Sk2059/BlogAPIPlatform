import pytest


@pytest.mark.asyncio
async def test_like_post(client, access_token):

    response = await client.post(
        "/likes/1",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Post liked successfully"