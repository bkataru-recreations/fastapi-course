from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import User as UserSchema, ShowUser as ShowUserSchema
from ..models import User as UserModel
from ..database import get_db
from ..utils import hash_password

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", response_model=ShowUserSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    new_user = UserModel(
        name=user.name, email=user.email, password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=ShowUserSchema)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    return user
