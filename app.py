#import libraries and custom scraping 
import os
from flask import Flask, render_template, redirect, url_for, redirect, request
from flask_pymongo import PyMongo
import scrape_space
import numpy as np
import pandas as pd
from pymongo import MongoClient 


app = Flask(__name__, template_folder= "templates")
 
#db 
# Local
app.config["MONGO_URI"] = "mongodb://localhost:27017/info"
#production: 
# MONGO_URI= os.environ.get('MONGO_URI')
# app.config["MONGO_URI"] = ENV['MONGO_URI']
mongo = PyMongo(app)

# client = MongoClient(MONGO_URI)
# db = client['heroku_zz25v35h']
#collection = db.visitorInfo


#routes
@app.route('/')
def index():
    # define info query to find the info  
    info = mongo.db.info.find_one()
    #render template and pass info from db in 
    return render_template("index.html", info = info)


@app.route("/scrape")
def scraper():
    #info in mongo
    info = mongo.db.info
    #scrape
    info_data = scrape_space.scrape()
    #add to mongo 
    info.replace_one({}, info_data, upsert=True)
    # redirect to /
    return redirect("/", code=302)



if __name__ == '__main__':
    app.run(debug=True)