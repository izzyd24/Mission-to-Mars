# new file to use flask and mongodb

import pandas as pd
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping


# set up flask 
app = Flask(__name__)

# connect py to mongo 
# app.config tells py that our app will connect to mongo via URI
# the uri is the local host link... app can reach mongo through our local host server with a port, named mars_app
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# set up routes for flask 

# ROUTE #1 for html page
# tell Flask to display home page, index.html
@app.route("/")
# def function to accomplish...
def index():
   # find mars collection within database
   # assign path to mars var to reference easily
   mars = mongo.db.mars.find_one()
   # tell flask to return html template using our index.html file
   # mars = mars tells python to use mars collection in mongodb
   return render_template("index.html", mars=mars)

# ROUTE #2 for scraping process
# defines the route Flask will use
# scrape will run the function
@app.route("/scrape")
# define it
def scrape():
   # assign new var to point to mongo database from earlier 
   mars = mongo.db.mars
   # new var to hold newly scraped data on the scraping.py file
   mars_data = scraping.scrape_all()
   # gathered the data, so now we update the database with updateone function
   # TYPICAL FORMAT: .update_one(query_param, {$set: data}, options)
   # we add data if not recorded previously
   # upser = true to tell mongo to create new doc if one doesn't exist
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   # once scraped, navigate back to page with updated content
   return redirect('/', code=302)

# tell flask to run
if __name__ == "__main__":
   app.run()