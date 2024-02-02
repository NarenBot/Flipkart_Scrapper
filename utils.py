import os
import csv
import pymongo


def get_require_fields(searchString, commentboxes, price_element):
    reviews = []
    i = 0
    j = len(commentboxes) - 1

    for commentbox in commentboxes:
        price = price_element[0].text

        if i < j:
            name_element = commentbox.div.div.find_all(
                "p", {"class": "_2sc7ZR _2V5EHH"}
            )[0]
            name = name_element.text

            rating_element = commentbox.div.div.div.div
            rating = rating_element.text

            headline_element = commentbox.div.div.div.p
            headline = headline_element.text

            comment_element = commentbox.div.div.find_all("div", {"class": ""})[0]
            comment = comment_element.text
            i += 1
        else:
            continue

        mydict = {
            "Price": price,
            "Product": searchString,
            "Customer-Name": name,
            "Rating": rating,
            "Heading": headline,
            "Comment": comment[:-9],
        }
        reviews.append(mydict)

    return reviews


def insert_data_csv(searchString, reviews):
    # Inserting Datas in CSV file
    os.makedirs("data", exist_ok=True)
    filename = os.path.join("data", searchString + ".csv")
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        headers = [
            "Price",
            "Product",
            "Customer-Name",
            "Rating",
            "Heading",
            "Comment",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(reviews)


def insert_data_mongo(reviews):
    # Inserting Datas in Mongo Atlas
    client = pymongo.MongoClient(
        "mongodb+srv://naren:root@clusterflip.bukguae.mongodb.net/?retryWrites=true&w=majority"
    )
    db = client["scrap_flipkart"]
    review_col = db["scrap_review"]
    review_col.insert_many(reviews)
