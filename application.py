import os
import time
from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin

# import requests
# from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from logger import logging
from utils import get_require_fields, insert_data_csv, insert_data_mongo


application = Flask(__name__)
app = application

DRIVER_PATH = "chromedriver.exe"


@app.route("/", methods=["GET"])
@cross_origin()
def index():
    logging.info("Home Page Launched !!!")
    return render_template("index.html")


@app.route("/scrapper", methods=["GET", "POST"])
@cross_origin()
def scrap():
    if request.method == "POST":
        try:
            driver = webdriver.Chrome(DRIVER_PATH)
            searchString = request.form["content"].replace(" ", "")
            flip_url = "https://www.flipkart.com/search?q=" + searchString
            logging.info(flip_url)

            driver.get(flip_url)
            flip_source = driver.page_source
            flip_html = bs(flip_source, "html.parser")
            bigboxes = flip_html.find_all("div", {"class": "_1AtVbE col-12-12"})
            logging.info(len(bigboxes))
            del bigboxes[0:2]

            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a["href"]
            driver.get(productLink)
            product_source = driver.page_source
            driver.quit()

            product_html = bs(product_source, "html.parser")
            commentboxes = product_html.find_all("div", {"class": "_16PBlm"})
            price_element = product_html.find_all("div", {"class": "_30jeq3 _16Jk6d"})

            reviews = get_require_fields(searchString, commentboxes, price_element)

            insert_data_csv(searchString, reviews)
            # insert_data_mongo(reviews)

            return render_template("results.html", reviews=reviews)

        except Exception as e:
            return f"Something went wrong: {e}"


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
