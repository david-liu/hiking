import sys
import datetime
from core.job_site_parser import JobSiteParser



class QiaobutangSiteParser(JobSiteParser):
    
    def __init__(self):
        super(QiaobutangSiteParser, self).__init__(url='http://job.qiaobutang.com/')
    
    def _get_field_css_selectors(self):
        return {
            "job_name" :  '.job-intro .job-intro__title',
            "updated_date" : '.job-intro .job-intro__bottom  .job-intro__bottom_right .job-intro__info_content',
            "location" : '.job-info .job-info-addr',
            "deadline" : '',
            "company" : '.job-intro .job-subtitle',
            "industry" : '.job-sidebar .job-sidebar__company_bottom .job-sidebar__slogan .job-require'
        }
    
    def _list_detail_page_urls(self, browser):
        elems = browser.find_elements_by_css_selector(".job__tab.job__tab_top .job__item a.job__title")

        urls = []
        for elem in elems:
            urls.append(elem.get_attribute("href"))
        
        # only return 10 urls for test
        return urls[:10]

    def _get_field_element_processors(self):
        processors = {
            'updated_date' : self._update_date_element_processor
        }
        return processors
        
        
    def _update_date_element_processor(self, element):
        raw_date = element.text

        return datetime.datetime.strptime(raw_date, '%Y-%m-%d')