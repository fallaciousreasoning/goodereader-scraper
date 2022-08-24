# Goodereader Scraper

This repository contains tools for sorting and filtering available ereaders. I wrote it to help me decide which ereader to buy afer my Kindle Voyage finally died.

## Usage

Install requirements:

    pip install -r requirements.txt

Run the program:

    python3 filter.py --query "ppi=300;waterproof=ipx;color temperature=Yes" --print price,weight,title --sort price,weight

This will filter to ereaders

    1. with 300 ppi
    2. Which have some ipx water proof rating
    3. and which support color temperature
Note: The `=` does not actually mean equal. The value on the right is used to make a case insensitive regex which is tested against the ereader's property value.

The results will be printed in a table with price,title and weight.

The results will be sorted by

    1. Price
    2. then weight, where the price is the same.

It will generate the following output:
```
+---------+--------+---------------------------------------------------------+
| price   | weight | title                                                   |
+---------+--------+---------------------------------------------------------+
| $249.99 | 192 g  | Kobo Libra H2O                                          |
| $259.99 | 300 g  | Pocketbook Inkpad 3 PRO                                 |
| $269.99 | 275 g  | Barnes and Noble Nook Glowlight Plus 7.8                |
| $314.99 | 188 g  | Amazon Kindle Oasis 3 with adjustable warm light (8GB)  |
| $329.99 | 188 g  | Amazon Kindle Oasis 3 with adjustable warm light (32GB) |
| $349.99 | 197 g  | Rakuten Kobo Forma e-Reader 8GB                         |
| $389.99 | 197 g  | Rakuten Kobo Forma e-Reader 32GB                        |
+---------+--------+---------------------------------------------------------+
```

Note: The first time the program is run, it may take some time, as it has to scrape the products from the good ereader store. The cache is maintained indefinitely, but you can force a rescrape by deleting `public/products.json`

To find the supported properties to query, have a look at the `public/products.json` file.

Force a rescrape:

    python3 scrape.py

Browse the WebUI

   npx serve public

Should start a server at http://localhost:3000
