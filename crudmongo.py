
from flask import Flask, request, jsonify ,Response
import os
import sys
import json
import pymongo
import bson
from bson import json_util
app=Flask(__name__)
####################databases #######

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
########insert records ############
@app.route("/insert", methods=["GET","POST"])

def insert_records() :
   
    #user=[ { '_id': 19, 'item': "large box", 'qty': 20 }]
    user=request.get_json()
    print(user)
    print(type(user))
    try :
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
    except :
       print("Something else went wrong")
       output = {'Status': 'Duplicate key',
                        '_id':user["_id"]}
       return output

#################### search records #############

@app.route("/search", methods=["GET","POST"])

def search_records() :
   
    #user={"Name":"vikas"}
    user=request.get_json()
    print(user)
    dbRespone=db.users.find(user,{'_id':0})
   # output = [{item: data[item] for item in data if item != '_id'} for data in dbRespone]
    l=[]
    for record in dbRespone:    
         l.append(record)
         print(l)
    return json.dumps(l ,default=json_util.default)
       
#################### update records ################

@app.route("/update", methods=["GET","POST"])
def update_records() :
    #user={"Name" : "ranjit","last_name" : "mogane"}
    user=request.get_json()
    split_idx =1
    print(user)
    myquery = dict(list(user.items())[:split_idx])
    newvalues = dict(list(user.items())[split_idx:])
    print(myquery)
    print(newvalues)
    dbRespone=db.users.update_many(myquery,{'$set':newvalues},)
    output = {'Status': "documents updated.",
                  'Document_count': str(dbRespone.modified_count)}
    return output

##################### delete records ######
@app.route("/delete", methods=["GET","POST"])
def delete_records() :
    #user={"Name" : "ranjit","last_name" : "mogane"}
    user=request.get_json()
    dbRespone=db.users.delete_many(user)
    output = {'Status': "documents deleted.",
                  'Document_count': str(dbRespone.deleted_count)}
    return output



if __name__== "__main__" :
    app.run(debug=True,port=8000)

