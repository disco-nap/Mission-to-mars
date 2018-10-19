from flask import Flask, render_template, jsonify, redirect
import sys
import pymongo
import scrape

#create instance of the flask app
sys.setrecursionlimit(2000)
app = Flask(__name__)

#create mongo connection
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_data_update

@app.route("/")
def home():
    mars_data = list(db.collection.find())
    return  render_template('index.html', mars_data=mars_data)


@app.route("/scrape")
def data_scrape():
    db.collection.remove({})
    mars_data = scrape.scrape()
    db.collection.insert_one(mars_data)
    return  render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
