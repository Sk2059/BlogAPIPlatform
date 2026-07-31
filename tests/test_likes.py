# import pytest

# @pytest.mark.asyncio
# async def test_like_post(client, access_token):

#     # Create post
#     post_response = await client.post(
#         "/posts",
#         headers={
#             "Authorization": f"Bearer {access_token}"
#         },
#         json={
#             "title": "Like Test",
#             "content": "Testing likes"
#         }
#     )

#     assert post_response.status_code == 201

#     post_id = post_response.json()["id"]

#     # Like it
#     response = await client.post(
#         f"/likes/{post_id}",
#         headers={
#             "Authorization": f"Bearer {access_token}"
#         }
#     )

#     assert response.status_code == 201

#     data = response.json()

#     assert data["message"] == "Post liked successfully"