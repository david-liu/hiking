import sys
import datetime
from core.job_site_parser import JobSiteParser

class ShixisengSiteParser(JobSiteParser):
    
    def __init__(self):
        super(ShixisengSiteParser, self).__init__(url='http://www.shixiseng.com')
    
    def _get_field_css_selectors(self):
        return {
            "job_name" :  '.jb_det_left .job_name',
            "updated_date" : '.jb_det_left .update_time',
            "location" : '.jb_det_left .city',
            "deadline" : '.closing_date + .date',
            "company" : '.jb_det_right .jb_det_right_top > a + p',
            "industry" : '.jb_det_right .jb_det_right_top .domain'
        }
    
    def _list_detail_page_urls(self, browser):
        elems = browser.find_elements_by_css_selector('.jib_inf_inf')
        urls = []

        for elem in elems:
            jobName_link = elem.find_element_by_css_selector("a.under_ani_jobname")
            urls.append(jobName_link.get_attribute("href"))
        
        return urls
    
    def _get_field_element_processors(self):
        processors = {
            'updated_date' : self._update_date_elelment_processor,
            'industry' : self._industry_element_processor,
            'deadline' : self._deadline_element_processor
        }
        return processors
        
        
    def _update_date_elelment_processor(self, element):
        raw_date = element.text
        if len(raw_date) > 2:
            date_text =  raw_date[:-2]
        else:
            date_text = raw_date

        return datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')

    def _deadline_element_processor(self, element):
        raw_date = element.text

        return datetime.datetime.strptime(raw_date, '%Y-%m-%d')
    
    def _industry_element_processor(self, element):
        raw_text = element.text
        return raw_text.split(",")
