# -*- coding: utf-8 -*-
import scrapy
import time
from urllib.parse import urljoin
from ..helper.text_processing import TextProcessing

class FrenchChamberSpider(scrapy.Spider):
    name = 'frenchchamber'
    start_urls = ['http://www.fccihk.com/members-directory/']

    # start_urls = ['http://www.fccihk.com/members-directory/'] +\
    #     ['http://www.fccihk.com/members-directory?page=%s&activity=all&search=all&membership=all' % page for page in range(1,20)]
    
    do_text_postprocessing = True

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
        # put line(s) of address into one line,
        # and strip all unnecessary \t and \n
        # in the front and back side of the address info
        if len(company_info['loc']) > 1:
            company_info['loc'] = '\n'.join([addr_per_line.strip() for addr_per_line in company_info['loc']])
        else:
            company_info['loc']  = company_info['loc']
        company_info['loc'] = company_info['loc'].strip()

        if len(company_info['desc']) > 1:
            company_info['desc'] = '\n'.join([addr_per_line.strip() for addr_per_line in company_info['desc']])
        else:
            company_info['desc']  = company_info['desc']
        company_info['desc'] = company_info['desc'].strip()

        # the "contact_info" sometimes filled with
        # unnecessary empty <li> that contains merely whitespace
        contact_info = []
        for line in company_info['contact']:
            line = line.strip()
            if len(line) > 0:
                contact_info.append(line)
        company_info['contact'] = contact_info

        # change list (that will consists of only one element) to string 
        # e.g. : change ```  'name': ['David']``` into ```'name' : 'David`  ```
        KEY_LIST_TO_STRING = ['name', 'logo_url']
        for key in KEY_LIST_TO_STRING:
            if company_info[key] != [] and company_info[key] != None:
                company_info[key] = company_info[key][0]
            else:
                company_info[key] = None

        # extract integer from string
        # e.g. : extract ```23``` from ```  '23 worldwide' ``` string.
        KEY_LIST_TO_BE_EXCTRACTED = ['year_established', 'local_employee', 'worldwide_employee']
        for key in KEY_LIST_TO_BE_EXCTRACTED:
            if company_info[key] == []:
                company_info[key] = None
            else:
                to_int = [int(s) for s in company_info[key][0].split() if s.isdigit()]
                if to_int == []:
                    company_info[key] = None
                else:
                    company_info[key] = to_int
        for key in KEY_LIST_TO_BE_EXCTRACTED:
            print(company_info[key])
            if company_info[key] != [] and company_info[key] != None:
                company_info[key] = company_info[key][0]
            else:
                company_info[key] = None


        # in employee_info, change list (that will consists of only one element) to string 
        # e.g. : change ```  'name': ['David']``` into ```'name' : 'David`  ```
        KEY_LIST_TO_STRING = ['job_title', 'first_name', 'last_name', 'photo_url']
        for employee_no in range(len(company_info['employees'])):
            for key in KEY_LIST_TO_STRING:
                if company_info['employees'][employee_no][key] == []:
                    # this happen if an employee doesn't have photo_url for example (photo_url = [])
                    company_info['employees'][employee_no][key] = ""
                else:
                    company_info['employees'][employee_no][key] = company_info['employees'][employee_no][key][0]

        return company_info