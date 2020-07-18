import argparse
import re
from scrape import get_all_product_info

product_info = get_all_product_info()

def get_props(reader, keys):
    return tuple(map(lambda k: reader[k], keys))

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

        if query[key] is True:
            continue

        ereader_value: str = ereader[key]
        matches = re.findall(query[key], ereader_value, re.IGNORECASE)
        if not matches:
            return False

    return True

def sort_readers(readers, by):
    return sorted(readers, key=lambda reader: get_props(reader, by))

def filter_readers(readers, query):
    for reader in readers:
        if matches_query(reader,query):
            yield reader

def print_readers(readers, keys):
    row_format = "{:>15}" * len(keys)
    print(row_format.format(keys))
    for reader in readers:
        props = get_props(reader, keys)
        print(row_format.format(props))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query')
    parser.add_argument('--sort', default='price')
    parser.add_argument('--print', default='price,title,url')

    args = parser.parse_args()
    query = parse_query(args.query)
    print(query)
    
    readers = get_all_product_info()
    sorted_readers = sort_readers(readers, args.sort.split(','))
    filtered_readers = list(filter_readers(sorted_readers, query))
    print(f'Found {len(filtered_readers)} reader(s):')
    print_readers(filter_readers, args.print.split(','))
