from flask import Blueprint
from flask import request
import time
import jwt
import json
import csv

user = Blueprint("user", __name__)

def validate(auth_token):
    """returns none if authentication is successful"""

    try:
        decoded = jwt.decode(auth_token, key="imperium")
    except:
        return json.dumps({"result":"Authentication Failed", "message":"unidentified token"})

    if not decoded["time"] > time.time():
        return json.dumps({"result":"authentication failed", "message":"token expired"})

    with open("data/user.csv", 'r') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    if not any(decoded["name"] == i["name"] for i in l):
        return json.dumps({"result":"authentication failed", "message":"invalid token"})

@user.route("/register", methods=["POST"])
def register():
    headers = ["id", "name", "email", "password", "contact_number", "address"]
    with open("data/user.csv", 'r') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    if any(int(i["id"]) == request.json["id"] for i in l):
        return json.dumps({"result":"registrartion failed", "message":"user already exists"})

    l.append({"id":request.json["id"], "name":request.json["name"], "email":request.json["email"], "password":request.json["password"], "contact_number":request.json["contact_number"], "address":request.json["address"]})
    
    with open("data/user.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(l)

    return json.dumps({"result":"registration successful"})

@user.route("/login", methods=["POST"])
def login():
    name = request.json["name"]
    password = request.json["password"]
    
    with open("data/user.csv", 'r') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    if not any((i["name"] == name and i["password"] == password) for i in l):
        return json.dumps({"result":"login failed", "message":"invalid credentials"})

    auth_token = jwt.encode({"name":name, "password":password, "time":time.time()+3600}, key="imperium").decode()  

    return json.dumps({"result":"login successful", "auth_token":auth_token})

@user.route("/modify", methods=["PATCH"])
def modify():
    res = validate(request.json["auth_token"])
    if res is not None:
        return res
    
    headers = ["id", "name", "email", "password", "contact_number", "address"]
    decoded = jwt.decode(request.json["auth_token"], key="imperium")

    with open("data/user.csv", 'r') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    for i in l:
        if i["name"] == decoded["name"]:
            i["password"] = request.json["new_password"]

    with open("data/user.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(l)

    return json.dumps({"result":"user modified successfully"})

@user.route("/delete/<name>", methods=["DELETE"])
def delete(name):
    res = validate(request.json["auth_token"])
    if res is not None:
        return res

    headers = ["id", "name", "email", "password", "contact_number", "address"]
    with open("data/user.csv", 'r', newline='') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    if name not in [i["name"] for i in l]:
        return json.dumps({"message":"no such user"})

    for i in l:
        if name == i["name"]:
            l.remove(i)

    with open("data/user.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(l)                

    return json.dumps({"result":"user deleted successfully"})    

@user.route("/get", methods=["GET"])
def user_details():
    res = validate(request.json["auth_token"])
    if res is not None:
        return res
    
    with open("data/user.csv", 'r', newline='') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    return json.dumps({"users":l})
    
