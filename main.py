import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, render_template
import json

app = Flask(__name__)

proxy = "203.115.101.55:80"

with open("working_proxies.txt", "r") as f:
    proxies = f.read().split("\n")

# proxies = {
#     "http": proxy,
#     "https": proxy
# }

urls = ["https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"]


def extract(proxy):
    try:
        r = requests.get('https://httpbin.org/ip', proxies={
            'http': proxy,
            'https': proxy
        })
        print(r.json(), ' - working')
    except Exception:
        pass
    return proxy


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
df.to_csv('data.csv')
