import threading
import queue

import requests

q = queue.Queue()
valid_proxies = []

with open("proxy_list.txt", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)


def check_proxies():
    global q

    with open("working_proxies.txt", "w") as file:
        while not q.empty():
            proxy = q.get()
            try:
                res = requests.get("http://ipinfo.io/json", proxies={
                    'http': proxy,
                    'https': proxy
                }, timeout=2)
            except Exception:
                print(f"Error with proxy {proxy}")
                continue

            if res.status_code == 200:
                print(f"Working proxy: {proxy}")
                file.write(proxy + "\n")
            else:
                print(f"Non-working proxy: {proxy}")


for _ in range(10):
    threading.Thread(target=check_proxies).start()
