
from flask import Flask, request, jsonify ,Response
import os
import sys
import json
import pymongo
import bson

app=Flask(__name__)
####################

try :
    # client = pymongo.MongoClient(host="localhost",
    #                              port=27017,
    #                              serverselectionTimeoutMS=1000)
    import pymongo
    client = pymongo.MongoClient('localhost',27017) 
    db=client["company"]
    client.server_info()  # trigger exception if cannot connect to db
    print(db)

except :
    print("error - server connect connect")

@app.route("/", methods=["GET","POST"])
def TEST() :
    return " testing  code "

@app.route("/insert", methods=["GET","POST"])

def insert_records() :
   
    #user=[ { '_id': 19, 'item': "large box", 'qty': 20 }]
    user=request.get_json()
    print(user)
    print(type(user))
    if type(user)== dict :
        dbRespone=db.users.insert_one(user)
        print(dbRespone.inserted_id)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(dbRespone.inserted_id)}
        return output
    else :
     dbRespone=db.users.insert_many(user)
     output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(dbRespone.inserted_ids)}
     return output
####################3

@app.route("/search", methods=["GET","POST"])

def search_records() :
   
    #user={"Name":"vikas"}
    user=request.get_json()
    dbRespone=db.users.find(user)
    #output = [{item: data[item] for item in data if item != '_id'} for data in dbRespone]
    for i in dbRespone :
        print(i)
    return i 
####################3

if __name__== "__main__" :
    app.run(debug=True,port=8000)

