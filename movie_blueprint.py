from flask import Blueprint
from flask import request
from user_blueprint import validate
import time
import jwt
import json
import csv

movie = Blueprint("movie", __name__)

@movie.route("/create", methods=["POST"])
def create_movie():
    res = validate(request.json["auth_token"])
    if res is not None:
        return res

    with open("data/user.csv", 'r') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    if request.json["user_id"] not in [int(i["id"]) for i in l]:
        return json.dumps({"result":"fail", "message":"invalid user id"})

    with open("data/movies.csv", 'r') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    if any(int(i["id"]) == request.json["id"] for i in l):
        return json.dumps({"result":"failed", "message":"movie already present"})  

    headers = ["id", "movie_name", "year", "duration", "user_id"]      
    l.append({"id":request.json["id"], "movie_name":request.json["movie_name"], "year":request.json["year"], "duration":request.json["duration"], "user_id":request.json["user_id"]})

    with open("data/movies.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(l)

    with open("data/category.csv", 'r', newline='') as f:
        reader = csv.DictReader(f)
        clist = list(reader)

    for i in request.json["category"]:
        found = False
        for j in clist:
            if j["category_name"] == i:
                cat_id = j["id"]
                found = True
                break
        if not found:
            cat_id = len(clist) + 1
        with open("data/category.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([cat_id, request.json["category"]])
        
        with open("data/movie_category.csv", 'r', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([cat_id]    
                

    return json.dumps({"result":"movie created successfully"})

@movie.route("/details", methods=["POST"])
def movie_details():
    res = validate(request.json["auth_token"])
    if res is not None:
        return res

    with open("data/movies.csv", 'r') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    return json.dumps({"movies":l})        

@movie.route("/search", methods=["POST"])
def search_movie():
    res = validate(request.json["auth_token"])
    if res is not None:
        return res

    with open("data/movies.csv", 'r') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    for i in l:
        if i["movie_name"] == request.json["movie_name"]:
            return json.dumps(i)

    return json.dumps({"result":"No such movie"})                

        
