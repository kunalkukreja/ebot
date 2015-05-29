Ebot
=======

Crawler bot for ecommerce sites. Use a base url and follows all category,grid and other links. Fetches data from product pages and writes to file. Currently only supports one spider


Installation
-------------

```
pip install scrapy
```

Set Up
-----
Change start_urls in each ebot/spiders/*spider.py file


Usage
-----

To write output to a json file 

```
scrappy crawl ebay -o camera.json
```
