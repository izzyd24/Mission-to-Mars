# new file to use flask and mongodb

import pandas as pd
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up flask 
app = Flask(_name_)

# connect py to mongo 
# app.config tells py that our app will connect to mongo via URI
# the uri is the local host link... app can reach mongo through our local host server with a port, named mars_app
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# set up routes for flask 

# 1st route for html page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

