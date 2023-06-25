from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi import Body, Response, status
from pydantic import BaseModel
from typing import Optional
from random import randrange
from bson.json_util import dumps

import pymongo
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional [int] = None

while True:
    try:
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["fastapi"]
        print(mydb)
        print("Database connection was successful")
        break
    except Exception as error:
        print(f"Database connection failed due to following error {error}")
        time.sleep(2)



def insert_doc(doc):
    mydb.seqs.update_one({ 'collection' : 'posts'},
                                        {'$inc': {'id': 1}})
    doc['created_at'] = datetime.now().timestamp()
    doc['id'] = mydb.seqs.find()[0]['id']
    print(mydb.seqs.find()[0]['id'])

    try:
        mydb.posts.insert_one(doc)

    except pymongo.errors.DuplicateKeyError as e:
        insert_doc(doc)


@app.get("/")
def root():
    return {"message": "Hello World233"}

@app.get("/posts")
def get_posts():
    py_post = mydb.posts.find({},{'_id':0})
    posts = []
    for post in py_post:
        posts.append(post)
    json_posts = dumps(posts)
    print(json_posts)
    return json_posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    insert_doc(post.dict())
    return{"data": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    post = mydb.posts.find_one( {'id':id },{'_id':0})
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with id: {id} not found"}
    return {"post_drtail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting post
    #find the index of the array of the specified id
    posts = mydb.posts.find_one( {'id':id })
    print(posts)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    mydb.posts.delete_one({'id' : id})
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = mydb.posts.find( {'id':id })
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    mydb.posts.replace_one({"id": id}, post.dict())
    return {"message": post}