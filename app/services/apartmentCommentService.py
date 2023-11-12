from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.apartmentComment import ApartmentCommentCreateSchema

from ..database import ApartmentComment
from enum import Enum
import uuid


class ApartmentCommentService:
    def __init__(self, db: Session):
        self.db = db

    async def create_comment(self, apartment_comment: ApartmentCommentCreateSchema):
        tag_create = ApartmentComment(
            id=str(uuid.uuid4()),
            user_id=apartment_comment.user_id,
            apartment_id=apartment_comment.apartment_id,
            text=apartment_comment.text,
        )
        self.db.add(tag_create)
        self.db.commit()
        self.db.refresh(tag_create)
        return tag_create

    async def get_comment_by_id(self, comment_id: str):
        return (
            self.db.query(ApartmentComment)
            .filter(ApartmentComment.id == comment_id)
            .first()
        )

    async def get_comments_by_apartment_id(self, apartment_id: str):
        return (
            self.db.query(ApartmentComment)
            .filter(ApartmentComment.apartment_id == apartment_id)
            .all()
        )

    async def update_comment(
        self, comment_id: str, apartment_comment: ApartmentCommentCreateSchema
    ):
        db_comment = await self.get_comment_by_id(comment_id)

        if not db_comment:
            raise HTTPException(status_code=404, detail="comment not found")

        for key, value in apartment_comment.model_dump(exclude_unset=True).items():
            setattr(db_comment, key, value)

        self.db.commit()
        self.db.refresh(db_comment)

        return db_comment

    async def delete_comment(self, comment_id: str):
        db_comment = await self.get_comment_by_id(comment_id)

        if not db_comment:
            raise HTTPException(status_code=404, detail="comment not found")

        self.db.delete(db_comment)
        self.db.commit()

        return "delete success"
