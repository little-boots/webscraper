from flask import Flask, render_template
import pymongo
from scraper import Scrape as scrape
import json


app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.store_inventory
collection = db.produce


@app.route("/scrape")
def index():
    content = scrape()

    return json.dumps(content)

if __name__ == "__main__":
    app.run(debug=True)
