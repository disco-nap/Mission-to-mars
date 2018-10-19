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
    mars_dict = list(db.collection.find())
    return  render_template('index.html', mars_dict=mars_dict)


@app.route("/scrape")
def data_scrape():
    db.collection.remove({})
    mars_dict = scrape.scrape()
    db.collection.insert_one(mars_dict)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
