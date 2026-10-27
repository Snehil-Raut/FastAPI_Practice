from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm  # use the built-in for username and pass verification from frontend -- during login
from typing import Annotated

router = APIRouter(tags=['Authentication'])


# post req as: user sends data
@router.post("/login", response_model=schemas.Token)
def login(user_creds: Annotated[OAuth2PasswordRequestForm, Depends()] , db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==user_creds.username).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Creds")
    
    # once username is correct check the password

    # pass the function name here "verify_pass"
    if not utils.verify_pass(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Creds")

    access_token = oauth2.create_acess_token(data={"user_id":user.id})  # just enciode userid, can add more

    return {"access_token": access_token, "token_type":"bearer" }


# VERFIYING IF THE TOKEN IS VALID
