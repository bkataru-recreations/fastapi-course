from typing import List
from fastapi import APIRouter, Depends, status, Request, Response, HTTPException
from sqlalchemy.orm import Session

from ..schemas import Blog as BlogSchema
from ..models import Blog as BlogModel

from ..database import get_db

router = APIRouter(prefix="/blogs", tags=["Blog"])


@router.get("/", response_model=List[BlogSchema])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()

    return blogs


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=BlogSchema)
def get_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog with such an id does not exist",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return "Such a blog does not exist"

    return blog


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogSchema, db: Session = Depends(get_db)):
    return blog
    # new_blog = BlogModel(title=blog.title, body=blog.body, user_id=1)

    # db.add(new_blog)
    # db.commit()
    # db.refresh(new_blog)

    # return new_blog


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, blog: BlogSchema, db: Session = Depends(get_db)):
    entry = db.query(BlogModel).filter(BlogModel.id == id).first()

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog does not exist"
        )

    entry.update()
    db.commit()

    return "updated"


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    entry = db.query(BlogModel).filter(BlogModel.id == id).first()

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog does not exist"
        )

    entry.delete(synchronize_session=False)
    db.commit()

    return
