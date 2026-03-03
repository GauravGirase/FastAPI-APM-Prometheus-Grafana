from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas
from ..utils import hash_passwd

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.get("/", status_code=status.HTTP_200_OK)
def get_post():
    return {"Users": "Users"}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = hash_passwd(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user