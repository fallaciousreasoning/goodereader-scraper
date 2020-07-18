import argparse
import re
from scrape import get_all_product_info
from prettytable import PrettyTable
import typing

product_info = get_all_product_info()

def lower_keys(items: typing.List[typing.Dict]):
    result = []

    for item in items:
        new_item = {}
        for key, value in item.items():
            new_item[key.lower()] = value
        result.append(new_item)

    return result

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
    table = PrettyTable()
    table.field_names = keys
    for key in keys:
        table.align[key] = 'l'

    for reader in readers:
        props = get_props(reader, keys)
        table.add_row(props)
    print(table)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query')
    parser.add_argument('--sort', default='price')
    parser.add_argument('--print', default='price,title')

    args = parser.parse_args()
    query = parse_query(args.query)
    print(query)
    
    readers = lower_keys(get_all_product_info())
    sorted_readers = sort_readers(readers, args.sort.split(','))
    filtered_readers = list(filter_readers(sorted_readers, query))
    print(f'Found {len(filtered_readers)} reader(s):')
    print_readers(filtered_readers, args.print.split(','))
