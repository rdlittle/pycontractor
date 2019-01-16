import sys
import pprint
from pymongo import MongoClient
from datetime import datetime

user_doc = {
    "username" : "johndoe",
    "firstname" : "John",
    "surname" : "Doe",
    "dateofbirth" : datetime(1966, 1, 2),
    "email" : "johndoe66@example.com",
    "score" : 0
}

client = MongoClient('localhost',27017)
db = client.admin
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
pprint.pprint(serverStatusResult)

#collection = db.users
#docId = collection.insert_one(user_doc).inserted_id
#docId
#users = collection.find({'username': 'johndoe'})
#for user in users:
#	print(user)
