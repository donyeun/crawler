# Web Scraper
In this repository, I crawled the French Chamber Hongkong website to scrap company informations which include company name, contact information, its location, number of employees both local and global, and also some informations regarding its employees such as name and job title. I used Scrapy Python package to make things easier. 

The data that the crawler returned are raw and may contained unnecessary contents here and there (eg.: trailing newline, consecutive space characters, and other unaesthetic information). For this reason, a text postprocessing helper is needed in order to clean the costemics of data.

## How to Run
1. Go to the folder where the code is being located.
```cd scrapy_crawler```

2. Install all the necessary Python packages. Please use `sudo` if necessary.
```pip3 install -r requirements.txt```

3. Run The `frenchchamber` crawler and save the resulted data into `frenchchamber.json`.
```scrapy crawl frenchchamber -t json --nolog -o - > frenchchamber.json```