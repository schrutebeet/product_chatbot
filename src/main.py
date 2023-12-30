import copy

from database.models import ECISupermarket, Mercadona
from database.utils_db import UtilsDB
from src.data_extractors.corte_ingles.eci_generic_extractor import ECIGenericExtractor
from src.data_extractors.corte_ingles.eci_supermarket_extractor import ECISupermarketExtractor
from src.data_extractors.mercadona.mercadona_extractor import MercadonaExtractor
from utils.default_columns import default_cols


def main():
    db_utils = UtilsDB()
    db_utils.create_new_models()
    data_extractor = ECIGenericExtractor("https://www.elcorteingles.es/api/firefly/vuestore/products_list/")
    for category in data_extractor.categories:
        category_dict = {}
        category_dict = data_extractor.iterate_thru_pages(category)
        category_model = db_utils.create_specific_model(category, category.replace("-", "_"), 'elCorteIngles', copy.deepcopy(default_cols))
        db_utils.insert_dict_in_db(category_dict, category_model)


    eci_supermarket = ECISupermarketExtractor("https://www.elcorteingles.es/alimentacion/api/catalog/get-page/supermercado")
    eci_supermarket = eci_supermarket.iterate_thru_pages()
    db_utils.insert_dict_in_db(eci_supermarket, ECISupermarket)

    mercadona_supermarket = MercadonaExtractor("https://tienda.mercadona.es/api/categories/")
    mercadona_supermarket = mercadona_supermarket.iterate_thru_categories()
    db_utils.insert_dict_in_db(mercadona_supermarket, Mercadona)

# CONSUM
# https://tienda.consum.es/api/rest/V1.0/shopping/category/menu
# https://tienda.consum.es/api/rest/V1.0/catalog/product?page=1&limit=20&offset=0&orderById=5&showRecommendations=false&categories=1690



if __name__ == "__main__":
    main()
