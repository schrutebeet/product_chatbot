import json

from src.data_extractor import DataExtractor

def main():
    data_extractor = DataExtractor("https://www.elcorteingles.es/api/firefly/vuestore/products_list/")
    data_dict = data_extractor.iterate_thru_pages("perfumeria")
    with open('my_dict.txt', 'w') as file:
        json.dump(data_dict, file, indent=4)


if __name__=="__main__":
    main()
