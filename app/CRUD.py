# THIS FILE DIRECTLY USES SQL COMMANDS TO INTERACT WITH POSTGRES

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row  #dict_row makes each result look like a dictionary
import time


app = FastAPI()

# using a while loop to 1st seacure the connection with DB, if any internet issues..it should keep trying to connect until DB is up. However, wrong password or worng username won't solve the problem

while True:
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapidb',
                            user='postgres', password='Snehil#7037',
                            row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except psycopg.Error as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)
    
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # default to True ,else user specified value -- From the body of Post(raw)
    #rating: Optional[int] = None  # int value is needed, else error from body

#################################################################################################################################
# WHEN  NO DATABASE AND INTERACT WITH INBUILD MEMEORY
# simple way to store post instead of database
# post_list = [{"title":"Titles 1", "content":"content of post1", "ID": 1},
#              {"title":"Favourite foods", "content":"multile cusine", "ID":2}]

# not a good way to get single post -- but for concept understanding
# def get_one_post(id):
#     for post in post_list:
#         if post["ID"] == id:
#             return post

# # delet a post from the list of posts
# def delete_post(id):
    
#     for i,p in enumerate(post_list):
#         if p['ID'] == id:  # if post id == id passed
#             return i
        
#     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"message: Post with ID {id} NOT FOUND" )  # IF ID is not present in list return 404
#################################################################################################################################


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
# gets all the posts from the data
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"Data": posts}

# try to get the latest post user added
@app.get("/posts/latest")
def latest_post():
    cursor.execute(""" SELECT * FROM posts ORDER BY created_at DESC LIMIT 1 """)
    latest_post = cursor.fetchone()

    if latest_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="message: Post NOT FOUND" )

    return {"Latest post": latest_post}


    # OLD CODE HARDOCDED
    # print("post list len", len(post_list))
    # if len(post_list) == 0:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"List is empty" )

    # new_post = post_list[-1]

    # return {f"latest post: {new_post}"}

# API to get single post from data 
@app.get("/posts{id}")  # link
def get_post(id: int):   #, response: Response):  # convert to int first -- if needed -- handels error on its own
    # NEW CODE WITH POSTGRES
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,)) # tuple so 1 extra comma
    get_post_id = cursor.fetchone()
    if not get_post_id:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"message: Post with {id} NOT FOUND" )
    return {"Data": get_post_id}

    # OLD CODE WITH HARDCODE DATA
    # post = get_one_post(id)
    # if not post:

    #     # wrap in 1 line
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"message: Post with {id} NOT FOUND" )

    #     # more than 1 line same code like above just extended
    #     # response.status_code = status.HTTP_404_NOT_FOUND   # if any single post is not present retrun 404
    #     # return {f"message: Post with {id} NOT FOUND"}
    # return f"Post details: {post}"

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(new_Post: Post):

    # We never do it the below way becoz from frontend if SQL Quesry is INJECTED it can manipulate the data -- SO to avoid SQL Command injection
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES ({posts.title}, {posts.content}, {posts.published})
    #                 RETURNING *""")
        
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s)
                    RETURNING *""", (new_Post.title, new_Post.content, new_Post.published))

    new_post = cursor.fetchone()  # above Return stored post to return
    conn.commit()                # COMMIT THE CHANGES / PUSH THE POST INTO THE DATA from the frontend
    return {"Data": new_post}

# DELETE
@app.delete("/posts/{id}")
def delete_apost(id: int):
    # NEW CODE
    cursor.execute(""" DELETE FROM posts WHERE id=%s 
                       RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"message: Post with {id} NOT FOUND" )

    conn.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)  # not to send anythin back

    # OLD CODE
    # index = delete_post(id)
    
    # post_list.pop(index)
    # return Response(status_code = status.HTTP_204_NO_CONTENT)  # not to send anythin back

# UPDATE
@app.put("/posts/{id}")
def update_post(id: int, post: Post):  # this line mentions that it should follow the given "Post" class

    cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
                   (post.title, post.content, post.published,id))

    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"message: Post with {id} NOT FOUND" )

    conn.commit()
    return {"Updated data": updated_post}

    # OLD CODE
    # index = delete_post(id)

    # post_dict = create_post.model_dump()  # get the data from the frontend
    # post_dict['ID'] = id                    # add the id new key
    # post_list[index] = post_dict          # so with the replce the current post@ a index to the new updated one
    # return {"Updated data": post_dict}