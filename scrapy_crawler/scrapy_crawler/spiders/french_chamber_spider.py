# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin

from ..helper.text_processing import TextProcessing

class FrenchChamberSpider(scrapy.Spider):
    """This class is a spider to crawl the French Chamber Hongkong website.
    The informations that are scraped are company name, logo URL, location, etc
    which also include details regarding employees (first and last name,
    job title, photo profile URL)
    """
    name = 'frenchchamber'
    # start_urls = ['http://www.fccihk.com/members-directory/']

    start_urls = ['http://www.fccihk.com/members-directory/'] +\
        ['http://www.fccihk.com/members-directory?page=%s&activity=all&search=all&membership=all' % page for page in range(1,20)]
    
    do_text_postprocessing = True
    text_proc = TextProcessing()

    def parse(self, response):
        company_relative_links = response.css('a.slide-cont::attr(href)').extract()
        for link in company_relative_links:
            company_profile_url = urljoin(response.url, link)
            yield scrapy.Request(company_profile_url, callback=self.parse_company_profile)


    def parse_company_profile(self, response):
        employee_html_info = response.css('div.members li')
        employee_info = []
        for element in employee_html_info:
            employee_info.append({
                'job_title' : element.css('div.job-title::text').extract(),
                'first_name':element.css('span.first-name::text').extract(),
                'last_name' :element.css('span.last-name::text').extract(),
                'photo_url' :element.css('img::attr(src)').extract()
            })
        
        company_info = {
            'name' : response.css('h1.page-title::text').extract(),
            'logo_url' : response.css('img.company-logo::attr(src)').extract(),
            'employees' : employee_info,
            'desc' : response.css('div.company-text *::text').extract(),
            'year_established' : response.selector.xpath('//h2[contains(text(), "Date of Establishment")]/following-sibling::p[1]/text()').extract(),
            'local_employee' : response.selector.xpath('//h2[contains(text(), "Number of Employees")]/following-sibling::p[contains(text(), "local")]/text()').extract(),
            'worldwide_employee' : response.selector.xpath('//h2[contains(text(), "Number of Employees")]/following-sibling::p[contains(text(), "worldwide")]/text()').extract(),
            'loc' : response.css('address::text').extract(),
            'contact' : response.css('ul.contact-info *::text').extract()
        }
        if self.do_text_postprocessing:
            yield self.text_postprocessing(company_info)
        else:
            yield company_info

    def text_postprocessing(self, company_info):
        # put line(s) of informations into one line,
        # and strip all unnecessary \t and \n located at
        # the front and back side of the address info
        KEY_LIST_TO_BE_CONCATENATED = ['loc', 'desc']
        for key in KEY_LIST_TO_BE_CONCATENATED:
            company_info[key] = self.text_proc.string_concatenate_list_of_informations(company_info[key])

        # the "contact" sometimes filled with
        # unnecessary empty <li> that contains merely whitespace
        KEY_LIST_REMOVE_NULL_ELEMENTS = ['contact']
        for key in KEY_LIST_REMOVE_NULL_ELEMENTS:
            company_info[key] = self.text_proc.remove_null_element_within_list(company_info[key])

        # change list (that will consists of only one element) to string 
        # e.g. : change ```  'name': ['David']``` into ```'name' : 'David`  ```
        KEY_LIST_TO_STRING = ['name', 'logo_url']
        for key in KEY_LIST_TO_STRING:
            company_info[key] = self.text_proc.convert_one_elm_list_into_string(company_info[key])

        # extract integer from string
        # e.g. : extract ```23``` from ```  '23 worldwide' ``` string.
        KEY_LIST_TO_BE_EXCTRACTED = ['year_established', 'local_employee', 'worldwide_employee']
        for key in KEY_LIST_TO_BE_EXCTRACTED:
            company_info[key] = self.text_proc.extract_integer_from_string(company_info[key])

        # in employee_info, change list (that will consists of only one element) to string 
        # e.g. : change ```  'name': ['David']``` into ```'name' : 'David`  ```
        KEY_LIST_TO_STRING = ['job_title', 'first_name', 'last_name', 'photo_url']
        for employee_no in range(len(company_info['employees'])):
            for key in KEY_LIST_TO_STRING:
                company_info['employees'][employee_no][key] = self.text_proc.convert_one_elm_list_into_string(company_info['employees'][employee_no][key])

        return company_info