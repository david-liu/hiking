import datetime
from core.run_config import RunConfig


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
    elems = browser.find_elements_by_css_selector('.jib_inf_inf')
    urls = []

    for elem in elems:
        jobName_link = elem.find_element_by_css_selector("a.under_ani_jobname")
        urls.append(jobName_link.get_attribute("href"))
        
    return urls

def _update_date_elelment_processor(element):
    raw_date = element.text
    if len(raw_date) > 2:
        date_text =  raw_date[:-2]
    else:
        date_text = raw_date

    return datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')

def _deadline_element_processor(element):
    raw_date = element.text

    return datetime.datetime.strptime(raw_date, '%Y-%m-%d')
    
def _industry_element_processor(element):
    raw_text = element.text
    return raw_text.split(",")


def _location_element_processor(element):
    return element.get_attribute("title").strip()

def create_run_config():

    return RunConfig(
        site_url=SITE_URL,
        field_css_selectors=CSS_SELECTORS,
        list_detail_page_urls_fn=_list_detail_page_urls,
        field_element_processors={
            'updated_date' : _update_date_elelment_processor,
            'location' : _location_element_processor,
            'industry' : _industry_element_processor,
            'deadline' : _deadline_element_processor})
        