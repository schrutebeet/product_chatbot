import requests
import time
import random

class DataExtractor:

    DICT_KEYS = ['title', 'product_name', 'coming_soon', 'eci_exclusive', 'exclusive', 'express', 'express_delivery', 'new', 'brand', 
                 'official_price', 'current_price', 'discount_percent', 'currency', 'provider', 'link', 'image_link']
    
    def __init__(self, url: str) -> None:
        self.url = url
        self.user_agent = {'User-agent': 'Mozilla/5.0'}
        self.data_dict = {key: [] for key in self.DICT_KEYS}

    def iterate_thru_pages(self, section: str) -> dict:
        done_pages = 1
        first_product_url = self.url + "/" + section + f"/{done_pages}"
        response = requests.get(first_product_url, headers = self.user_agent, timeout=10)
        items_per_page = response.json()['data']['pagination']['itemsPerPage']
        time.sleep(random.randint(2, 4))
        while response.status_code == 200:
            r_json = response.json()
            self._handle_json(r_json, items_per_page)
            done_pages += 1
            time.sleep(random.randint(1, 3))
            page_url = self.url + "/" + section + f"/{done_pages}"
            response = requests.get(page_url, headers = self.user_agent, timeout=10)
        return self.data_dict

    def _handle_json(self, r_json: dict, items_per_page: int):
        for item in range(items_per_page):
            self.data_dict['title'].append(r_json['data']['products'][0]['categories'][0]['name'])
            self.data_dict['product_name'].append(r_json['data']['products'][item]['title'])
            self.data_dict['coming_soon'].append(r_json['data']['products'][item]['badges']['coming_soon'])
            self.data_dict['eci_exclusive'].append(r_json['data']['products'][item]['badges']['eci_exclusive'])
            self.data_dict['exclusive'].append(r_json['data']['products'][item]['badges']['exclusive'])
            self.data_dict['express'].append(r_json['data']['products'][item]['badges']['express'])
            self.data_dict['express_delivery'].append(r_json['data']['products'][item]['badges']['express_delivery'])
            self.data_dict['new'].append(r_json['data']['products'][item]['badges']['new'])
            self.data_dict['brand'].append(r_json['data']['products'][item]['brand']['name'])
            self.data_dict['current_price'].append(r_json['data']['paginatedDatalayer']['products'][item]['price'].get('f_price'))
            self.data_dict['official_price'].append(r_json['data']['paginatedDatalayer']['products'][item]['price'].get('o_price', self.data_dict['current_price'][-1]))
            self.data_dict['discount_percent'].append(r_json['data']['paginatedDatalayer']['products'][item]['price'].get('discount_percent'))
            self.data_dict['currency'].append(r_json['data']['paginatedDatalayer']['products'][item]['price']['currency'])
            self.data_dict['provider'].append(r_json['data']['products'][item]['provider']['name'])
            self.data_dict['link'].append(r_json['data']['products'][item]['_base_url'])
            self.data_dict['image_link'].append(r_json['data']['products'][item]['image']['default_source'])
