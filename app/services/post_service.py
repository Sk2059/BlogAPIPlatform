from datetime import datetime,timezone
import re

from fastapi import HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post , PostStatus
from app.models.user import User

from app.repositories.post_repository import PostRepository

from app.schemas.post import (
    PostCreate,
    PostUpdate,
    PostStatusUpdate
)

class PostService:

    @staticmethod
    async def generate_slug(title:str)->str:
        slug = title.lower()
        slug = re.sub(r"[^a-z0-9\s-]", "", slug)
        slug = re.sub(r"\s+","-",slug)
        return slug.strip("-")

    @staticmethod 
    async def generate_unique_slug(
        db:AsyncSession,
        title:str
    ):
        base_slug = await PostService.generate_slug(title)

        slug = base_slug

        counter = 1

        while await PostRepository.get_by_slug(
            db,
            slug
        ):
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug


    @staticmethod
    async def create_post(
        db:AsyncSession,
        data:PostCreate,
        current_user:User
    ):
        slug = await PostService.generate_unique_slug(
            db,
            data.title
        )

        post = Post(
            title=data.title,
            slug=slug,
            content=data.content,
            excerpt=data.excerpt,
            cover_image=data.cover_image,
            author_id=current_user.id
        )
        return await PostRepository.create(db, post)


    @staticmethod
    async def get_post(
        db: AsyncSession,
        post_id: int
    ):
        post = await PostRepository.get_by_id(
            db,
            post_id
        )

        if not post:

            raise HTTPException(
                status_code=404,
                detail="Post not found"
            )

        return post

    @staticmethod
    def verify_owner(
        post: Post,
        current_user: User
    ):

        if post.author_id != current_user.id:

            raise HTTPException(
                status_code=403,
                detail="You do not have permission to modify this post."
            )

    @staticmethod
    async def update_post(
        db:AsyncSession,
        post_id:str,
        data:PostUpdate,
        current_user:User
    ):
        post = await PostService.get_post(
            db,
            post_id
        )

        PostService.verify_owner(
            post,
            current_user
        )

        updates = data.model_dump(
            exclude_unset=True
        )

        for key, value in updates.items():
            setattr(post, key, value)

        if "title" in updates:
            post.slug = await PostService.generate_unique_slug(
                db,
                post.title
            )

        return await PostRepository.update(
            db,
            post
        )

    @staticmethod
    async def delete_post(
        db,
        post_id,
        current_user
    ):

        post = await PostService.get_post(
            db,
            post_id
        )

        PostService.verify_owner(
            post,
            current_user
        )

        await PostRepository.delete(
            db,
            post
        )

    @staticmethod
    async def update_status(
        db: AsyncSession,
        post_id: int,
        status_data: PostStatusUpdate,
        current_user: User
    ):
        post = await PostService.get_post(
                    db,
                    post_id
                )

        PostService.verify_owner(
                    post,
                    current_user
                )
        
        post.status = status_data.status

        if status_data.status == PostStatus.PUBLISHED:
            post.published_at = datetime.now(
                timezone.utc
            )

        return await PostRepository.update(
                db,
                post
            )

    @staticmethod
    async def list_posts(
        db,
        skip,
        limit
    ):
        return await PostRepository.list_published(
            db,
            skip,
            limit
        )

    @staticmethod
    async def my_posts(
        db,
        current_user,
        skip,
        limit
    ):

        return await PostRepository.list_by_author(
            db,
            current_user.id,
            skip,
            limit
        )

    @staticmethod 
    async def get_post_by_slug(
            db: AsyncSession,
            slug: str
        ):
            post = await PostRepository.get_by_slug
            (
                db,
                slug
            )
            if not post:
                raise HTTPException(
                    status_code=404,
                    detail="Post not found"
                )
    
            return post

    @staticmethod
    async def search_posts(
        db,
        search,
        skip,
        limit
    ):

        return await PostRepository.search_posts(
            db,
            search,
            skip,
            limit
        )