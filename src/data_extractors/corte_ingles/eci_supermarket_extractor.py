import json
import random
import time
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from config.log_config import logger
from utils.headers import headers


class ECISupermarketExtractor:
    DICT_KEYS = [
        "timestamp",
        "date",
        "id",
        "product_name",
        "category_1",
        "category_2",
        "category_3",
        "category_4",
        "brand",
        "original_price",
        "final_price",
        "discount",
        "status",
        "currency",
    ]

    def __init__(self, url: str) -> None:
        self.url = url
        self.data_dict = {key: [] for key in self.DICT_KEYS}

    def iterate_thru_pages(self) -> dict:
        done_pages = 1
        keep_loop = True
        logger.info("Started data fetching for ECI's supermarket.")
        while keep_loop:
            product_url = self.url + f"/{done_pages}"
            response = requests.get(product_url, headers=random.choice(headers), timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")
            products_list = json.loads(soup.find("div")["data-json"])["products"]
            keep_loop = self._iterate_thru_product_list(products_list)
            logger.debug(f"Stored information from page {done_pages}.")
            done_pages += 1
            time.sleep(random.randint(1, 3))
        logger.info("Finished data fetching for ECI's supermarket.")
        logger.info(f"Pages scraped: {done_pages - 1}.")
        return self.data_dict

    def _iterate_thru_product_list(self, product_list: List[dict]) -> bool:
        if product_list:
            for product in product_list:
                _time = datetime.utcnow()
                self.data_dict["timestamp"].append(_time)
                self.data_dict["date"].append(_time.strftime("%Y-%m-%d"))
                self.data_dict["id"].append(product["id"].strip("_"))
                self.data_dict["product_name"].append(product.get("name"))
                self.data_dict["brand"].append(product.get("brand"))
                self.data_dict["final_price"].append(product.get("price").get("final"))
                self.data_dict["original_price"].append(product.get("price").get("original", self.data_dict["final_price"][-1]))
                self.data_dict["discount"].append(product.get("discount"))
                self.data_dict["status"].append(product.get("status"))
                self.data_dict["currency"].append(product.get("currency"))
                product["category"] = self.ensure_four_elements(product.get("category"))
                if product["category"]:
                    category_count = 1
                    for n in range(4):
                        self.data_dict[f"category_{str(category_count)}"].append(product["category"][n])
                        category_count += 1
                    keep_loop = True
        else:
            keep_loop = False
        return keep_loop

    @staticmethod
    def ensure_four_elements(list_: list):
        additional_elements = 4 - len(list_)
        if additional_elements > 0:
            list_.extend([None] * additional_elements)
        return list_
