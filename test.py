from flask import Flask, render_template
import pymongo
from scraper import Scrape as scrape
import json


conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars
collection = db.scrape

#init_content = scrape()
#db.collection.insert_one(init_content)

content = list(db.collection.find())[-1:][0]
print(content)
