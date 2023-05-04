import json
import uuid
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify

URL = "https://webcaycanh.com/"
SCRIPT_DIR = Path(__file__).parent.absolute()
MEDIA_DIR = SCRIPT_DIR / Path("media")
MEDIA_DIR.mkdir(exist_ok=True)
DEBUG = True


def get_product_info(p_url):
    print(f"Crawling {p_url}")
    r = requests.get(p_url)
    soup = BeautifulSoup(r.content, "lxml").select_one("div#left-panel")

    try:
        name = soup.select_one(".tit-h1").text.strip()
        price = soup.select_one(".gia-cay").text.removesuffix("đ").replace(",", "")
        summary = soup.select_one(".text-justify").text
        thumbnail = soup.select_one("#sync1 > div > img").attrs["data-lazy-src"]
        description = soup.select_one("#contentsp > p:nth-child(1)").text.strip()

        info = {}

        info["name"] = name
        info["price"] = price
        info["summary"] = summary
        info["thumbnail"] = thumbnail
        info["description"] = description
        return info
    except Exception:
        print("Errors")
        return None


def get_products(category_url, cate_id):
    print(f"Crawling {cate_id}")
    product_urls = []

    for i in range(1, 10):
        r = requests.get(f"{category_url}/page/{i}")
        soup = BeautifulSoup(r.content, "lxml")
        product_tags = soup.select("div.item-loop-tour")
        for product_tag in product_tags:
            url = product_tag.select_one("a").attrs["href"]
            product_urls.append((url, cate_id))

    return product_urls


# div.col-md-4:nth-child(1)
def get_filename(image_url: str):
    extension = image_url.split(".")[-1]
    return uuid.uuid1().hex + "." + extension


def download_image(url: str, filename: Path):
    print(f"Downloading {url} to {filename}")
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in r:
                f.write(chunk)


if __name__ == "__main__":
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, "lxml")

    category_tags = soup.select("div.col-sm-6 > a")

    fixgure = []

    p_id = 1

    for i, category_tag in enumerate(category_tags, start=1):
        name = category_tag.attrs["title"]
        url = category_tag.attrs["href"]
        image = category_tag.select_one("img").attrs["data-lazy-src"]
        slug = slugify(name)
        now = datetime.now()
        filename = get_filename(image)

        category = {}
        category["model"] = "core.category"
        category["pk"] = i
        category["fields"] = {
            "name": name,
            "slug": slug,
            "image": filename,
            "created_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "updated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        fixgure.append(category)

        products_url = get_products(url, i)
        for p_url, cate_id in products_url:
            info = get_product_info(p_url)

            if info is None:
                continue

            product = {}
            product["model"] = "core.product"
            product["pk"] = p_id
            p_id += 1
            p_filename = get_filename(info["thumbnail"])
            download_image(info["thumbnail"], MEDIA_DIR / p_filename)
            product["fields"] = {
                "name": info["name"],
                "price": info["price"],
                "summary": info["summary"],
                "thumbnail": p_filename,
                "description": info["description"],
                "category": cate_id,
                "quantity": 100,
                "created_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "updated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

            fixgure.append(product)

        download_image(image, MEDIA_DIR / filename)
        get_products(url, i)
        if DEBUG:
            print(json.dumps(category, indent=4))
            print(filename)
        else:
            print("Crawled", i, name)

    with open("fixtures.json", "w") as f:
        json.dump(fixgure, f, indent=4, ensure_ascii=False)
