import pytest


@pytest.mark.asyncio
async def test_update_profile(client, access_token):

    response = await client.patch(
        "/users/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "full_name": "Sabinam Mahato",
            "bio": "Backend Developer",
            "location": "Nepal"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["full_name"] == "Sabinam Mahato"
    assert data["bio"] == "Backend Developer"
    assert data["location"] == "Nepal"