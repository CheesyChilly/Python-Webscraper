from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

app = Flask(__name__)


proxy = "203.115.101.55:80"


@app.route('/')
def index():
    urls = [
        "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"]
    info = []

    # counter = 0
    # for site in urls:
    #     try:
    #         print(f"Using the proxy: {proxies[counter]}")
    #         res = requests.get(site, proxies={'http': proxies[counter],
    #                                           'https': proxies[counter]})
    #         print(res.status_code)
    #         print(res.text)
    #     except Exception:
    #         print("failed")
    #     finally:
    #         counter = (counter + 1) % len(proxies)

    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        books = soup.find_all(class_="product_pod")

        for book in books:
            titles = book.find("h3").find("a")["title"]
            rating = book.find("p")["class"][1]
            price = book.find(class_="price_color").text
            price = float(price[2:])
            info.append([titles, rating, price])
    df = pd.DataFrame(info, columns=['Title', 'Star Rating', 'Price'])
    csv_path = os.path.join(os.getcwd(), 'dataFromFlask.csv')
    df.to_csv(csv_path, index=False)

    return render_template('index.html', info=info)


if __name__ == '__main__':
    app.run(debug=True)
