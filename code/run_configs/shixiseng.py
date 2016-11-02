from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from hiking.utils import parser_helper, url_helper
from hiking.core.run_config import ByKeys, FieldTypeKeys, FieldMultiplicityKeys, RunConfig


SITE_URL = 'http://www.shixiseng.com'

CSS_SELECTORS = {
    "job_name" :  '.jb_det_left .job_name',
    "updated_date" : '.jb_det_left .update_time',
    "location" : '.jb_det_left .city',
    "deadline" : '.closing_date + .date',
    "company" : '.jb_det_right .jb_det_right_top > a + p',
    "industry" : '.jb_det_right .jb_det_right_top .domain'
}

def _list_detail_page_urls(browser):
    urls = []
    urls.extend(_get_hotjob_urls(browser))
        #urls.extend(_get_hotcompany_job_urls(browser))
    return urls

def _get_hotjob_urls(browser):

    elems = browser.find_elements_by_css_selector('.jib_inf_inf')
    urls = []
    for elem in elems:
        jobName_link = elem.find_element_by_css_selector("a.under_ani_jobname")
        urls.append(jobName_link.get_attribute("href"))
    return urls

def _get_hotcompany_job_urls(browser):
    companyUrls = []
    elems = browser.find_elements_by_css_selector('#hot_job .hot_inf_box')
    for elem in elems:
        companyUrls.append(SITE_URL + elem.get_attribute("data-href"))

    jobUrls = []
    for url in companyUrls:
        # logger.info('crawl company url: %s', url)
        urls = _get_company_hotjob_urls(browser, url)
        jobUrls.extend(urls)

    return jobUrls

def _get_company_hotjob_urls(browser, companyUrl):
    browser.get(companyUrl)
    urls = []
    elems = browser.find_elements_by_css_selector('.jib_inf_inf')
    for elem in elems:
        link = elem.find_element_by_css_selector('a')
        # logger.info('link: %s', link.get_attribute("href"))
        urls.append(link.get_attribute("href"))
    return urls

def _update_date_elelment_processor(element):
    raw_date = parser_helper.get_element_text(element)
    if len(raw_date) > 2:
        date_text =  raw_date[:-2]
    else:
        date_text = raw_date

    return parser_helper.format_to_date_string(date_text, 
        src_format='%Y-%m-%d %H:%M:%S')

def _deadline_element_processor(element):
    raw_date = parser_helper.get_element_text(element)

    return parser_helper.format_to_date_string(raw_date, 
        src_format='%Y-%m-%d')

def _industry_element_processor(element):
    raw_text = parser_helper.get_element_text(element)
    return raw_text.split(",")[0]


def _location_element_processor(element):
    return element.get_attribute("title").strip()

def create_run_config():

    return RunConfig(
        site_url=SITE_URL,
        field_selectors=CSS_SELECTORS,
        list_detail_page_urls_fn=_list_detail_page_urls,
        block_selector='.box',
        field_element_processors={
            'updated_date' : _update_date_elelment_processor,
            'location' : _location_element_processor,
            'industry' : _industry_element_processor,
            'deadline' : _deadline_element_processor})
