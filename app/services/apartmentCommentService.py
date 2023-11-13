from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
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
            rate_location=apartment_comment.rate_location,
            rate_amenities=apartment_comment.rate_amenities,
            rate_interior=apartment_comment.rate_interior,
            rate_price=apartment_comment.rate_price,
        )

        self.db.add(tag_create)
        self.db.commit()
        self.db.refresh(tag_create)

        total_rate = round(
            (
                apartment_comment.rate_location
                + apartment_comment.rate_amenities
                + apartment_comment.rate_interior
                + apartment_comment.rate_price
            )
            / 4,
            1,
        )

        tag_create.total_rate = total_rate

        return tag_create

    async def get_comment_by_id(self, comment_id: str):
        return (
            self.db.query(ApartmentComment)
            .filter(ApartmentComment.id == comment_id)
            .first()
        )

    async def get_comments_by_apartment_id(self, apartment_id: str):
        comments = (
            self.db.query(ApartmentComment)
            .options(joinedload(ApartmentComment.user))
            .filter(ApartmentComment.apartment_id == apartment_id)
            .order_by(desc(ApartmentComment.created_at))
            .all()
        )

        num_comments = len(comments)

        if num_comments == 0:
            return {
                "total_rate_price": 0.0,
                "total_rate_amenities": 0.0,
                "total_rate_location": 0.0,
                "total_rate_interior": 0.0,
                "comments": [],
            }

        total_rate_price = sum(comment.rate_price for comment in comments)
        total_rate_amenities = sum(comment.rate_amenities for comment in comments)
        total_rate_location = sum(comment.rate_location for comment in comments)
        total_rate_interior = sum(comment.rate_interior for comment in comments)

        statistical = {
            "total_rate_price": round(total_rate_price / num_comments, 1),
            "total_rate_amenities": round(total_rate_amenities / num_comments, 1),
            "total_rate_location": round(total_rate_location / num_comments, 1),
            "total_rate_interior": round(total_rate_interior / num_comments, 1),
            "comments": comments,
        }

        for comment in comments:
            comment.total_rate = round(
                (
                    comment.rate_price
                    + comment.rate_amenities
                    + comment.rate_location
                    + comment.rate_interior
                )
                / 4
            )

        return statistical

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
