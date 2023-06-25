import pymongo
from datetime import datetime

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")

db = myclient["fastapi"]
print(db)
print(myclient.list_database_names())

def insert_doc(doc):
    db.seqs.update_one({ 'collection' : 'posts'},
                                        {'$inc': {'id': 1}})
    doc['created_at'] = datetime.now().timestamp()
    doc['id'] = db.seqs.find()[0]['id']
    print(db.seqs.find()[0]['id'])

    try:
        db.posts.insert_one(doc)

    except pymongo.errors.DuplicateKeyError as e:
        insert_doc(doc)

insert_doc({"title": "Title1", "content": "Content1", "published": True})
insert_doc({"title": "Title2", "content": "Content2", "published": True})
