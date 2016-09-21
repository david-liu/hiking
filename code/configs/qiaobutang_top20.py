import datetime
from core.run_config import RunConfig


SITE_URL = 'http://job.qiaobutang.com/'

CSS_SELECTORS = {
    "job_name" :  '.job-intro .job-intro__title',
    "updated_date" : '.job-intro .job-intro__bottom  .job-intro__bottom_right .job-intro__info_content',
    "location" : '.job-info .job-info-addr',
    "deadline" : '',
    "company" : '.job-intro .job-subtitle',
    "industry" : '.job-sidebar .job-sidebar__company_bottom .job-sidebar__slogan .job-require'
}

def _list_detail_page_urls(browser):
    elems = browser.find_elements_by_css_selector(".job__tab.job__tab_top .job__item a.job__title")

    urls = []
    for elem in elems:
        urls.append(elem.get_attribute("href"))
        
    # only return 10 urls for test
    return urls[:10]

def _update_date_element_processor(element):
    raw_date = element.text

    return datetime.datetime.strptime(raw_date, '%Y-%m-%d')

def create_run_config():
    
    return RunConfig(
        site_url=SITE_URL,
        field_css_selectors=CSS_SELECTORS,
        list_detail_page_urls_fn=_list_detail_page_urls,
        field_element_processors={
            'updated_date' : _update_date_element_processor
        })