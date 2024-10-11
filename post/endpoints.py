from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import scoped_session
from sqlalchemy import and_
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request

from auth.security import manager, limiter  # noqa

from core.database import get_session  # noqa
from post.models import Post  # noqa
from post.schemas import PostSchema, CreatePostRequestSchema, CreatePostResponseSchema, UpdatePostRequestSchema, UpdatePostResponseSchema  # noqa

router = APIRouter()


@router.post("/", response_model=CreatePostResponseSchema)
@limiter.limit("100/minute")
async def create_post(
        request: Request,
        data: CreatePostRequestSchema,
        db: scoped_session = Depends(get_session),
        user=Depends(manager)
):
    """
    Create new post
    """
    post = Post(**data.model_dump(), user_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.patch('/{post_id}', response_model=UpdatePostResponseSchema)
@limiter.limit("100/minute")
async def update_post(
        request: Request,
        post_id: UUID,
        data: UpdatePostRequestSchema,
        db: scoped_session = Depends(get_session),
        user=Depends(manager)
):
    """
    Update post
    """
    post = db.query(Post).filter(
        and_(
            Post.id == post_id,
            Post.user_id == user.id
        )
    ).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    obj_data = jsonable_encoder(post)
    update_data = data.model_dump(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(post, field, update_data[field])
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get('/', response_model=list[PostSchema])
@limiter.limit("100/minute")
async def get_posts(
        request: Request,
        db: scoped_session = Depends(get_session),
        user=Depends(manager)
):
    """
    Get all posts
    """
    return db.query(Post).all()


@router.get('/{post_id}', response_model=PostSchema)
@limiter.limit("100/minute")
async def get_post_by_id(
        request: Request,
        post_id: UUID,
        db: scoped_session = Depends(get_session),
        user=Depends(manager)
):
    """
    Get post by id
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return HTTPException(
            status_code=404,
            detail="Post not found"
        )
    return post


@router.delete('/{post_id}')
@limiter.limit("100/minute")
async def delete_post(
        request: Request,
        post_id: UUID,
        db: scoped_session = Depends(get_session),
        user=Depends(manager)
):
    """
    Delete post
    """
    post = db.query(Post).filter(
        and_(
            Post.id == post_id,
            Post.user_id == user.id
        )
    ).delete()
    if post == 0:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    return {"id": post_id}
