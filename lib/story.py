# coding=utf-8
import urllib
import urllib3
import certifi
import re
import datetime

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"


def get_story(query):
    if re.match("^https?://s\.aliexpress.com/", query):
        query = get_real_link(query)

    if re.match("^\d+$", query):
        query = "https://ru.aliexpress.com/item/item/{}.html".format(query)
    params = {
        "fpsub": 1,
        "from": "index",
        "keyword": query
    }

    url = "/?" + urllib.urlencode(params)
    print url
    currency = "RUB"

    headers = get_headers()

    pool = get_pool()
    response = pool.request("GET", url, headers=headers)

    data = response.data
    matches = re.findall("(myData.push\(\[)(\d+), (\d+\.?\d{0,2})", data)
    result = []

    for m in matches:
        ts = float(m[1])
        d = datetime.datetime.fromtimestamp(ts)
        v = {
            "date": d,
            "val": m[2],
            "currency": currency
        }
        result.append(v)
    return result


def get_real_link(query):
    query = query.replace("http://s.aliexpress.com", "")
    query = query.replace("https://s.aliexpress.com", "")
    pool = get_pool("s.aliexpress.com")
    response = pool.request("HEAD", query, headers=get_headers(), retries=False)
    return response.headers["Location"]


def get_pool(hostname="www.aliprice.com"):
    return urllib3.HTTPSConnectionPool(hostname, ca_certs=certifi.where(), maxsize=5, port=443)


def get_headers():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "User-Agent": user_agent
    }
