from fastapi import APIRouter, Response, status, HTTPException, Depends
from .. import models, schemas, utils, oauth2 # . = curr directory
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

# API router 
router = APIRouter(
    prefix="/posts",   # to avoid uncessary repetation of paths
    tags= ['Posts']
)


@router.get("/")
async def root():
    return {"message": "Hello World"}

# gets all the posts from the data
@router.get("/all",response_model=List[schemas.PostOut])
#router.get("/all")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int=3, skip: int=0, search: Optional[str]=""):   # limit is the num of posts we fetched from frontend. # skip if user wants to skip x no of posts from start.., # search will get what user wants to search
    # post = db.query(models.Post).all()  # query tell which specifc model.tablename 

    #post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  # this will by default fetch x num of posts given by user

    posts= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote ,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return [ {"post":posts, "votes": votes} for posts,votes in posts  ]

# try to get the latest post user added
@router.get("/latest", response_model=schemas.PostOut)
def latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #new_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    new_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote ,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).order_by(models.Post.created_at.desc()).first()
    if new_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="message: Post NOT FOUND" )

    post, votes = new_post
    return  {"post":post, "votes": votes}


# API to get single post from data 
# / posts + /id = /posts/id
@router.get("/{id}", response_model=schemas.PostOut)  # link
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):   #, response: Response):  # convert to int first -- if needed -- handels error on its own, 

    #get_id_post = db.query(models.Post).filter(models.Post.id==id).first()  #anytime we know we have to fetch single item use ".first()"

    get_id_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote ,models.Vote.post_id == models.Post.id, isouter=True).filter(models.Post.id==id).group_by(models.Post.id).first()
    if not get_id_post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    post, votes = get_id_post
    return  {"post":post, "votes": votes}

# POST a new post in the data
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(new_Post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # forcing user to logged in b4 creating post
    # unpack the dict which comes from frontend -- so no need to follow the 83 line code

    new_post = models.Post(owner_id=current_user.id, **new_Post.model_dump()) # efficient way, also associates the post directly to the user
    # not efficient way -- what if we have many cols/fields
    #new_post = models.Post(title=new_Post.title, content=new_Post.content, published=new_Post.published )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # this is sqlalchemy model
    return new_post

# DELETE
@router.delete("/{id}")
def delete_apost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # also check while deleting is the user himself is the owner to dlete the post
    delete_query = db.query(models.Post).filter(models.Post.id==id)
    delete_post = delete_query.first()

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    delete_query.delete(synchronize_session=False)
    db.commit()         # commit the changes

    return Response(status_code = status.HTTP_204_NO_CONTENT)  # not to send anythin back

# UPDATE
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # this line mentions that it should follow the given "Post" class

    # saving the query
    update_post = db.query(models.Post).filter(models.Post.id==id)
    db_post = update_post.first()  # grab the post if exist

    if db_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"message: Post with {id} NOT FOUND" )

    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # if exisit grab the query and update it
    update_post.update(post.model_dump() ,synchronize_session=False)
    db.commit()
    return update_post.first() # get the updated post -- the first which matches

