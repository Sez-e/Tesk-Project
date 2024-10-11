from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PostSchema(BaseModel):
    """
    Post Schema.
    """
    id: UUID
    text: str
    created_at: datetime
    updated_at: datetime


class CreatePostRequestSchema(BaseModel):
    """
    Create Post request Schema.
    """
    text: str


class CreatePostResponseSchema(BaseModel):
    """
    Create Post response Schema.
    """
    id: UUID
    text: str
    created_at: datetime


class UpdatePostRequestSchema(BaseModel):
    """
    Update Post request Schema.
    """
    text: str | None = None


class UpdatePostResponseSchema(BaseModel):
    """
    Update Post response Schema.
    """
    id: UUID
    text: str
    updated_at: datetime
