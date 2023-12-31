import random
import time
from datetime import datetime

import requests

from config.log_config import logger
from utils.headers import headers


class ECIGenericExtractor:
    DICT_KEYS = [
        "timestamp",
        "date",
        "id",
        "title",
        "product_name",
        "coming_soon",
        "eci_exclusive",
        "exclusive",
        "express",
        "express_delivery",
        "new",
        "brand",
        "original_price",
        "final_price",
        "discount_percent",
        "currency",
        "provider",
        "link",
        "image_link",
    ]

    def __init__(self, url: str) -> None:
        self.url = url
        self.categories = self.find_categories()
        self.categories_underscore = [category.replace("-", "_") for category in self.categories]

    def find_categories(self) -> list:
        list_categories = []
        response = requests.get(self.url, headers=random.choice(headers))
        r_json = response.json()
        categories = r_json['data']['filters']['_menubar'][0]['values']
        for category in categories:
            list_categories.append(category['slugs'][0])
        return list_categories

    def iterate_thru_pages(self, section: str) -> dict:
        info_dict = {key: [] for key in self.DICT_KEYS}
        done_pages = 1
        first_product_url = self.url + "/" + section + f"/{done_pages}"
        response = requests.get(first_product_url, headers=random.choice(headers))
        items_per_page = response.json()["data"]["pagination"]["itemsPerPage"]
        time.sleep(random.randint(2, 4))
        logger.info(f'Started data fetching for ECI\'s "{section}" section.')
        while response.status_code == 200:
            r_json = response.json()
            are_products = r_json["data"]["products"]
            if not are_products:
                break
            self._handle_json(r_json, info_dict, items_per_page)
            logger.debug(f"Stored information from page {done_pages}.")
            done_pages += 1
            time.sleep(random.randint(1, 2))
            page_url = self.url + "/" + section + f"/{done_pages}"
            response = requests.get(page_url, headers=random.choice(headers))
        logger.info(f'Finished data fetching for ECI\'s "{section}" section.')
        logger.info(f"Pages scraped: {done_pages - 1}.")
        return info_dict

    def _handle_json(self, r_json: dict, info_dict: dict, items_per_page: int) -> dict:
        for item in range(items_per_page):
            _time = datetime.utcnow()
            if r_json["data"]["products"]:
                info_dict["timestamp"].append(_time)
                info_dict["date"].append(_time.strftime("%Y-%m-%d"))
                info_dict["id"].append(r_json["data"]["products"][item]["id"])
                info_dict["title"].append(r_json["data"]["products"][item]["categories"][0]["name"])
                info_dict["product_name"].append(r_json["data"]["products"][item].get("title"))
                info_dict["coming_soon"].append(r_json["data"]["products"][item]["badges"].get("coming_soon"))
                info_dict["eci_exclusive"].append(r_json["data"]["products"][item]["badges"].get("eci_exclusive"))
                info_dict["exclusive"].append(r_json["data"]["products"][item]["badges"].get("exclusive"))
                info_dict["express"].append(r_json["data"]["products"][item]["badges"].get("express"))
                info_dict["express_delivery"].append(r_json["data"]["products"][item]["badges"].get("express_delivery"))
                info_dict["new"].append(r_json["data"]["products"][item]["badges"].get("new"))
                info_dict["brand"].append(r_json["data"]["products"][item].get("brand", {}).get("name"))
                info_dict["final_price"].append(r_json["data"]["paginatedDatalayer"]["products"][item]["price"].get("f_price"))
                info_dict["original_price"].append(r_json["data"]["paginatedDatalayer"]["products"][item]["price"].get("o_price", info_dict["final_price"][-1]))
                info_dict["discount_percent"].append(r_json["data"]["paginatedDatalayer"]["products"][item]["price"].get("discount_percent"))
                info_dict["currency"].append(r_json["data"]["paginatedDatalayer"]["products"][item]["price"].get("currency"))
                info_dict["provider"].append(r_json["data"]["products"][item]["provider"].get("name"))
                info_dict["link"].append(r_json["data"]["products"][item].get("_base_url"))
                info_dict["image_link"].append(r_json["data"]["products"][item]["image"].get("default_source"))