from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi import FastAPI, Depends, HTTPException
from typing import Generator, List, Optional
from schemas import BookCreate, BookResponse

Base = declarative_base()
engine = create_engine('sqlite:///bookTable.db', connect_args={"check_same_thread": False})

class Book(Base):
    __tablename__ = 'Book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=False)
    author = Column(String(256), nullable=False)
    year = Column(Integer, nullable=True)

Base.metadata.create_all(engine)
SessionParent = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#sesion = Session()

def get_db() -> Generator[Session, None, None]:
    db = SessionParent()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    book_sql = Book(title=book.title, author=book.author, year=book.year)
    db.add(book_sql)
    db.commit()
    db.refresh(book_sql)
    return book_sql

@app.get("/books/", response_model=List[BookResponse])
def read_all_books(db: Session = Depends(get_db)):
    books = db.scalars(select(Book)).all()
    return books

@app.delete("/books/{book_id}", status_code=204)
def delete_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db.scalars(select(Book).where(Book.id == book_id)).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    db.delete(book)
    db.commit()
    return None

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    book_find = db.scalars(select(Book).where(Book.id == book_id)).first()
    if not book_find:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    book_find.title = book.title
    book_find.author = book.author
    book_find.year = book.year
    db.commit()
    return book_find

@app.get("/books/search/", response_model=List[BookResponse])
def read_books_with_params(
        author: Optional[str] = None,
        title: Optional[str] = None,
        year: Optional[int] = None,
        db: Session = Depends(get_db)
    ):
    select_books = select(Book)
    if author:
        select_books = select_books.where(Book.author == author)
    if title:
        select_books = select_books.where(Book.title == title)
    if year:
        select_books = select_books.where(Book.year == year)
    books = db.scalars(select_books).all()
    return books

@app.get("/healthcheck")
async def healthcheck() -> dict:
    return {"status": "ok"}

