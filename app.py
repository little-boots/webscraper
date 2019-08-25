from flask import Flask, render_template
import pymongo
from scraper import Scrape as scrape
import json


app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars
collection = db.scrape


@app.route("/")
def index():
    # Display whatever content is available
    content = list(db.collection.find())[-1:][0]

    return render_template("index.html", display_content=content)


@app.route("/scrape")
def scrape_():
    content = scrape()

    db.collection.insert_one(content)

    return json.dumps(content)


if __name__ == "__main__":
    app.run(debug=True)
