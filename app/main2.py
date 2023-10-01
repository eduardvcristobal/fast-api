from typing import Optional

import psycopg2
from psycopg2._psycopg import cursor
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Body, status, HTTPException
from fastapi.openapi.models import Response
from pydantic import BaseModel
# from pydantic.class_validators import Optional
from random import randint
import time

app = FastAPI()

class Post(BaseModel):
    id : Optional[int]
    title: str
    content: str
    published: Optional[bool] = False

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='postgres')
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

    # while True:
def connect_to_database():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='postgres',
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        print("Database connection was successfully established!")
        print (conn, cursor)
        return conn, cursor
    except Exception as error:
        print("Connecting to the database failed")
        print("Error: ", error)
        return None, None

def main():
    conn, cursor = connect_to_database()
    if conn and cursor:
        # You have a valid connection here, so you can perform database operations
        # For example:
        cursor.execute("SELECT * FROM public.products")
        results = cursor.fetchall()
        for row in results:
            print(row)

        # Don't forget to close the cursor and connection when done
        cursor.close()
        conn.close()


# connect_to_database()


my_posts=[
    {"title": "test title", "content": "test content 123", "id": 1},
    {"title": "test title 2", "content": "test content 123 2", "id": 2},
]

def find_post_by_id(id):
    for post in my_posts:
        if post["id"] == id:
            return post


@app.get("/")
async def root():
    return {"message": "Hello World"}

# -------------------------POSTGRES DATABASE-------------------------

@app.get("/db-getall-posts")
async def get_posts():
    cursor.execute("SELECT * FROM public.products")
    posts = cursor.fetchall()
    context = {"data": posts}
    return context


# -------------------------LOCAL DATA-------------------------
@app.post("/create-post", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post.id = randint(1, 100000)
    post_dict = post.dict()
    post_dict["id"] = randint(1, 100000)
    my_posts.append(post.dict())
    print(post_dict)
    return {"data": post_dict}

@app.post("/create-posts")
async def create_posts(posts: list[Post]):
    return {"data": posts}

# @app.put("/posts/{post_id}")
# async def update_post(post_id: int, post: Post):
#     json = {"data": {"title": "updated title", "content": "updated content"}}
#     print(json)
#     return json

@app.get("/posts/{id}")
async def get_post(id: int):
    print(type(id))
    post = find_post_by_id(id)
    if not post:
        return HTTPException(status_code=404, detail=f"Post not found with id {id}")
    return post

    # if not post:
    #     response.status_code = status.HTTP_404_NOT_FOUND


@app.get("/posts")
async def get_posts():
    # cursor.execute("""SELECT * FROM public.products""")
    # posts = cursor.fetchall()
    return {"data": my_posts}

@app.get("/posts-latest")
async def get_latest_post():
    return {"data": my_posts[-1]}


# @app.delete("/posts/{id}")
# async def delete_post(id: int):
#     post = find_post_by_id(id)
#     my_posts.remove(post)
#     return {"message": "Post with id {0} has been deleted.".format(id)}