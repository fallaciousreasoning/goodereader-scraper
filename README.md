# Goodereader Scraper

This repository contains tools for sorting and filtering available ereaders. I wrote it to help me decide which ereader to buy afer my Kindle Voyage finally died.

## Usage

Install requirements:

    pip install -r requirements.txt

Run the program:

    python3 filter.py --query "ppi=300;waterproof=ipx;color temperature=Yes" --print price,title,weight --sort price,weight

This will filter to ereaders

    1. with 300 ppi
    2. Which have some ipx water proof rating
    3. and which support color temperature
Note: The `=` does not actually mean equal. The value on the right is used to make a case insensitive regex which is tested against the ereader's property value.

The results will be printed in a table with price,title and weight.

The results will be sorted by

    1. Price
    2. then weight, where the price is the same.

Note: The first time the program is run, it may take some time, as it has to scrape the products from the good ereader store. The cache is maintained indefinitely, but you can force a rescrape by deleting `cache/products.json`

To find the supported properties to query, have a look at the `cache/products.json` file.