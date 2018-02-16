# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin

class FrenchChamberSpider(scrapy.Spider):
    name = 'frenchchamber'
    start_urls = ['http://www.fccihk.com/members-directory/']
    do_post_processing = True

    def parse(self, response):
        company_relative_links = response.css('a.slide-cont::attr(href)').extract()
        for link in company_relative_links:
            company_profile_url = urljoin(response.url, link)
            yield scrapy.Request(company_profile_url, callback=self.parse_company_profile)

    def parse_company_profile(self, response):
        company_info = {
            'company_name' : response.css('h1.page-title::text').extract(),
            'company_logo_link' : response.css('img.company-logo::attr(src)').extract(),
            # 'description' : response.css('div.company-text *::text').extract(),
            # 'employee_names_and_designation' : response.css('').extract(),
            # 'employee_image_link' : response.css('').extract(),
            'location' : response.css('address::text').extract(),
            'contact_info' : response.css('ul.social-links').extract()
        }
        if self.do_post_processing:
            yield self.post_processing(company_info)
        else:
            yield company_info

    def post_processing(self, company_info):
        # put line(s) of address into one line,
        # and strip all unnecessary \t and \n
        # in the front and back side of the address info
        if len(company_info['location']) > 1:
            company_info['location'] = '\n'.join([addr_per_line.strip() for addr_per_line in company_info['location']])
        else:
            company_info['location']  = company_info['location']
        return company_info