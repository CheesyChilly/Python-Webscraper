from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

app = Flask(__name__)


@app.route('/')
def index():
    urls = [
        "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html", "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"]
    info = []

    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        books = soup.find_all(class_="product_pod")

        for book in books:
            titles = book.find("h3").find("a")["title"]
            rating = book.find("p")["class"][1]
            prices = book.find(class_="price_color").text
            price = float(prices[2:])
            info.append([titles, rating, price])
    df = pd.DataFrame(info, columns=['Title', 'Star Rating', 'Price'])
    csv_path = os.path.join(os.getcwd(), 'data2.csv')
    df.to_csv(csv_path, index=False)

    return render_template('index.html', info=info)


if __name__ == '__main__':
    app.run(debug=True)
