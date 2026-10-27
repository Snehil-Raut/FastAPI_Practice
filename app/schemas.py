# this is our SCHEMA 
# Pydanic BaseModel serves as the foundation for defining structured, type-checked data objects. 
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import  Literal

class Post(BaseModel):  # BASEMODEL IS PYDANTIC MODEL , WE try to define the shape of our database
    title: str
    content: str
    published: bool = True # default to True ,else user specified value -- From the body of Post(raw)

# with the help of inheritance we are updating/creating post. Where above is parent class
class PostCreate(Post):
    pass

# any info of user when we want to GET the user info
class UserOut(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

# inherit the rest from base class
class PostResponse(Post):
    id: int
    owner_id: int
    owner   : UserOut       # this will tell who is the owner of a post
    model_config = ConfigDict(from_attributes=True)    # we tell pydantic model to read the data even if it is not a dict

class PostOut(BaseModel):
    post: PostResponse
    votes: int
    model_config = ConfigDict(from_attributes=True)    # we tell pydantic model to read the data even if it is not a dict
    

class UserCreate(BaseModel):
    # one valid way to check for right email address is to send link to the registered emailS
    email: EmailStr      # EmailStr automatically rejects invalid emails before they reach your logic
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for accesstoken and toketype
class Token(BaseModel):
    access_token: str
    token_type: str

# token data -- data in access token
class TokenData(BaseModel):
    id: int

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]   #direction