import argparse
import re
from scrape import get_all_product_info

product_info = get_all_product_info()

def parse_query(query):
    """Query looks like this: 
       "ppi=300;waterproof;backlight"

       Should return:
           {
               'ppi': 300,
               'waterproof': True,
               'backlight': True
           }
    """
    result = {}
    props = query.split(';')

    for prop in props:
        parts = prop.split('=')
        value = True if len(parts) == 1 else parts[1]
        result[parts[0]] = value

    return result

def matches_query(ereader, query):
    for key in query:
        if not key in ereader:
            return False

        ereader_value: str = ereader[key]
        matches = re.findall(query[key], ereader_value, re.IGNORECASE)
        if not matches:
            return False

    return True


def filter(query):
    for reader in product_info:
        if matches_query(reader,query):
            yield reader['title']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query')

    args = parser.parse_args()
    query = parse_query(args.query)
    print(query)
    print(list(filter(query)))
