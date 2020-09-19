from flask import Flask
from flask import Blueprint
from user_blueprint import user
from movie_blueprint import movie
import jwt
import json 
import csv

app = Flask(__name__)
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(movie, url_prefix='/movie')


@app.route('/')
def home():
    return "Welcome to home page"