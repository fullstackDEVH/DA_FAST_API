from sqlalchemy.orm import Session

from app.models import Book
from app.schemas import BookSchema


class CrudUser:
    def __init__(self, db: Session):
        self.db = db

    def get_book(seft, skip: int = 0, limit: int = 10):
        return seft.db.query(Book).offset(skip).limit(limit).all()

    def get_book_by_id(seft, book_id: int):
        return seft.db.query(Book).filter(Book.id == book_id).first()

    def create_book(seft, book: BookSchema):
        print(book)
        print(f"**book : {book.dict()}")
        _book = Book(**book.dict())

        seft.db.add(_book)
        seft.db.commit()
        seft.db.refresh(_book)
        return _book

    def remove_book(seft, book_id: int):
        _book = get_book_by_id(db=seft.db, book_id=book_id)
        seft.db.delete(_book)
        seft.db.commit()

        return "success"

    def update_book(seft, book_id: int, book: BookSchema):
        _book = get_book_by_id(db=seft.db, book_id=book_id)
        _book.title = book.title
        _book.desc = book.desc
        seft.db.commit()
        seft.db.refresh(_book)
        return _book
