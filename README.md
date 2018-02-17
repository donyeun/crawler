# crawler

This is a program to crawl. In this code, I scraped French Chamber Hongkong website. I used Scrapy Python package to make things easier. 

## Steps
The data that I got from crawler are raw and contained unnecessary contents (eg.: trailing newline, consecutive space characters, and other unaesthetic information.)

## How to Run
``` scrapy crawl frenchchamber -o test.json```
Please remember to delete the json file first, as it appends the prior content of the json file.