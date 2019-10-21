#import libraries and custom scraping 
from flask import Flask, render_template, redirect, url_for, redirect, request
from flask_pymongo import PyMongo
import scrape_space
import numpy as np
import pandas as pd


app = Flask(__name__, template_folder= "templates")

#db 
app.config["MONGO_URI"] = "mongodb://localhost:27017/info"
mongo = PyMongo(app)


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