from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def get_post():
    return {"Datas": "Posts"}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def create_posts(post: schemas.PostBase, db: Session = Depends(get_db)):
    '''
    new_post = models.Post(title=post.title,
                           content=post.content,
                           published=post.published)
    '''
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found !")
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} doesn't exists !")
    
    post.delete(synchronize_session=False)

@router.patch("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} doesn't exists !")
    
    print(dir(post))
    print(post)
    post_query.update(post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return post_query.first()