from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
# use pymongo to set up the connection to the database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)


@app.route("/")
def index():
    # access information from the database
    mars_data = mongo.db.marsData.find_one()
    print(mars_data)
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    #References to a database collection (table)
    marsTable = mongo.db.marsData

    #Drop the table if it exists
    mongo.db.marsData.drop()

    #Call scrape mars script
    mars_data = scrape_mars.scrape_all()

    #Take the dictionary and load it into mongoDB
    marsTable.insert_one(mars_data)

    #Go back to the index route
    return redirect("/")


if __name__ == "__main__":
    app.run()