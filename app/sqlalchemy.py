# THIS FILE USES SQLALCHMEY TO INTERACT WITH POSTGRES SQL
# All the ORM commands just runs SQL command at backend
from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post,user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine) # This line uses SQLAlchemy # creates all tables when started
# But ALEMBIC REPLACES THIS SO WE DONT NEED THIS
app = FastAPI()


# domain to talk to our api -- we can proivde our lists
# if origins=["*"]  --- means all domain wilol talk
origins=["*"]

app.add_middleware(
    CORSMiddleware,      # middleware is func which runs b4 any req -- performs some ops
    allow_origins=origins,   # which domains to talk with our API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)