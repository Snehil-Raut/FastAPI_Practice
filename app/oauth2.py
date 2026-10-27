# 3 pieces of info
# SECRET_KEY, # ALGORTIHM , # EXPIRATION TIME -- FOR NOT TO Login user forever
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#handle-jwt-tokens
import jwt
from jwt.exceptions import InvalidTokenError
from .import schemas, database, models
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings
# ENDPOINT OF LOGIN URL
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')  # login endpoint

# not a good idea to store secter key here -- later update it
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_acess_token(data: dict):
    # create a copy of users data
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # currenttime + expire time
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# verify the access token
def verify_access_token(token: str, credential_exception):   # Action is credzs dont mathc

    # the code could error out so try excpet bloxk
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])

        # extract data
        id = payload.get("user_id")

        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
    except InvalidTokenError:
        raise credential_exception

    return token_data  # id from line 42


# why this - once the verify access token return ID, the below function should fetch user from db -- so we can attach user to any path ops and perform logic
def get_current_user(token:str=Depends(oauth2_schema), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials"
                                          , headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user



# woprking of login 
# eg from the endpoint if user creates a post it will depend on the above functions to check if user is authorized