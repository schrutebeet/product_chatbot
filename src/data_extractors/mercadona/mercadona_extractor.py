import requests
import time
import random
from datetime import datetime
from fake_useragent import UserAgent

from config.log_config import logger
from utils.headers import headers


class MercadonaExtractor:
    DICT_KEYS = [
            "timestamp",
            "date",
            "id",
            "category_1",
            "category_2",
            "category_3",
            "product_name",
            "previous_unit_price",
            "unit_price",   # price per unit of product
            "unit_size",    # number of L, kg... for each unit of item
            "size_format",   # unit in which the "unit_size" is expressed (L, kg...)
            "iva",  # % VAT of the product
            "reference_price",  # price of the reference size (e.g., the 10 in 10€/1L)
            "reference_unit",   # reference unit for "reference_price" i.e., the "L" in "10€/1L"
            "total_units",  # units inside the item
            "is_new",
            "is_pack",
            "packaging",
            "link",
            "image_link",
        ]

    def __init__(self, url: str) -> None:
        self.url = url
        self.master_categories = {}
        self.data_dict = {key: [] for key in self.DICT_KEYS}

    def detect_categories(self) -> dict:
        header = {"User-agent": UserAgent().random}
        response = requests.get(self.url, headers=header)
        r_json = response.json()['results']
        for item in r_json:
            self._iterate_over_main_categories(item)
        return self.master_categories

    def _iterate_over_main_categories(self, category: dict) -> None:
        if 'categories' in category and isinstance(category['categories'], list):
            for sub_cat in category['categories']:
                self.master_categories[f"{sub_cat['id']}"] = [category['name'], sub_cat['name']]

    def iterate_thru_categories(self) -> dict:
        self.detect_categories()
        sections_fetched = 0
        total_sections = len(self.master_categories.keys())
        logger.info('Started data fetching all Mercadona\'s sections and sub-section.')
        for key, value in self.master_categories.items():
            logger.debug(f'Started data fetching for Mercadona\'s "{value}" sub-section. ({sections_fetched*100/total_sections:.2f}% extracted)')
            url_product_page = self.url + key
            response = requests.get(url_product_page, headers=random.choice(headers))
            r_json = response.json()['categories']
            for sub_sub_cat in r_json:  
                category_3 = sub_sub_cat['name']
                for product in sub_sub_cat['products']:
                    _time = datetime.utcnow()
                    self.data_dict["timestamp"].append(_time)
                    self.data_dict["date"].append(_time.strftime("%Y-%m-%d"))
                    self.data_dict['id'].append(product['id'])
                    for idx, category in enumerate(value):
                        self.data_dict[f"category_{idx + 1}"].append(category)
                    self.data_dict["category_3"].append(category_3)
                    self.data_dict['product_name'].append(product['display_name'])
                    self.data_dict['previous_unit_price'].append(product['price_instructions']['previous_unit_price'])
                    self.data_dict['unit_price'].append(product['price_instructions']['unit_price'])
                    self.data_dict['unit_size'].append(product['price_instructions']['unit_size'])
                    self.data_dict['size_format'].append(product['price_instructions']['size_format'])
                    self.data_dict['iva'].append(product['price_instructions']['iva'])
                    self.data_dict['reference_price'].append(product['price_instructions']['reference_price'])
                    self.data_dict['reference_unit'].append(product['price_instructions']['reference_format'])
                    self.data_dict['total_units'].append(product['price_instructions']['total_units'])
                    self.data_dict['is_new'].append(product['price_instructions']['is_new'])
                    self.data_dict['is_pack'].append(product['price_instructions']['is_pack'])
                    self.data_dict['packaging'].append(product['packaging'])
                    self.data_dict['link'].append(product['share_url'])
                    self.data_dict['image_link'].append(product['thumbnail'])
            sections_fetched += 1
            time.sleep(random.randint(2, 4))
        logger.info('Finished data fetching all Mercadona\'s sections and sub-section.')
        return self.data_dict

