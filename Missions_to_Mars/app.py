# import libraries
from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars
import sys

# CREATE AN INSTANCE FOR FLASK
app = Flask(__name__)

# USE PYMONGO TO ESTABLISH MONGO CONNECTION
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# ROUTE TO RENDER INDEX.HTML TEMPLATE USING DATA FROM MONGO
@app.route("/")
def home():

    mars_data = mongo.db.mars.find_one()

    return render_template("index.html", data=mars_data)

# ROUTE THAT WILL TRIGGER THE SCRAPE FUNCTION
@app.route("/scrape")
def scrape():  
    
    # RUN THE SCRAPE FUNCTION
    mars_scrape = scrape_mars.scrape_info()
    
    # UPDATE MONGO DATABASE USING UPDATE AND UPSERT=TRUE
    mongo.db.mars.update({}, mars_scrape, upsert=True)
    
    # REDIRECT BACK TO HOMEPAGE
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)