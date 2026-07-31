import pytest


@pytest.mark.asyncio
async def test_create_comment(client, access_token):

    response = await client.post(
        "/comments/",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "post_id": 1,
            "content": "Great article!"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["content"] == "Great article!"
    assert data["post_id"] == 1