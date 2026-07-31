# import pytest

# @pytest.mark.asyncio
# async def test_create_comment(client, access_token):

#     # Create a post first
#     post_response = await client.post(
#         "/posts",
#         headers={
#             "Authorization": f"Bearer {access_token}"
#         },
#         json={
#             "title": "Test Post",
#             "content": "Test Content"
#         }
#     )

#     assert post_response.status_code == 201

#     post_id = post_response.json()["id"]

#     # Create comment
#     response = await client.post(
#         f"/posts/{post_id}/comments",
#         headers={
#             "Authorization": f"Bearer {access_token}"
#         },
#         json={
#             "content": "Great article!"
#         }
#     )

#     assert response.status_code == 201

#     data = response.json()

#     assert data["content"] == "Great article!"
#     assert data["post_id"] == post_id