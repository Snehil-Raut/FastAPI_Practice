from .. import models, schemas, utils 
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


# API router 
router = APIRouter(
    prefix="/user",    # to avoid uncessary repetation of paths
    tags= ['Users']     # Filter the docs properly -- <link>/docs 
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the user password
    hashed_password = utils.Hash(new_user.password)
    new_user.password = hashed_password  # updates the pydantic user model
    new_User = models.User(**new_user.model_dump())

    db.add(new_User)
    db.commit()
    db.refresh(new_User)
    return new_User


@router.get("/{id}", response_model=schemas.UserOut)  # we don;t want to return the password
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if user == None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    return user