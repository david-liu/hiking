import utils.log_helper as logger
import utils.webelement_parser_helper as parser_helper
from core.run_config import ByKeys, FieldTypeKeys, FieldMultiplicityKeys
from core.run_config import RunConfig



SITE_URL = 'http://job.qiaobutang.com/'

CSS_SELECTORS = {
    "job_name" :  'h1.job-intro__title',
    "updated_date" : '.job-intro .job-intro__bottom  .job-intro__bottom_right .job-intro__info_content',
    "location" : '.job-info .job-info-addr',
    "deadline" : '',
    "company" : 'h2.job-subtitle',
    "industry" : '.job-sidebar .job-sidebar__company_bottom .job-sidebar__slogan .job-require'
}

# A exmple of complex selector
    
# CSS_SELECTORS = {
#     "job_name" :  {
#         'key': 'job-intro__title',
#         'by': ByKeys.CLASS_NAME
#     },
#     "updated_date" : '.job-intro .job-intro__bottom  .job-intro__bottom_right .job-intro__info_content',
#     "location" : '.job-info .job-info-addr',
#     "deadline" : '',
#     "company" : 'h2.job-subtitle',
#     "industry" : {
#         'key' : '.job-sidebar .job-sidebar__company_bottom .job-sidebar__slogan .job-require',
#         'multi' : FieldMultiplicityKeys.MANY
#     }
# }

def _list_detail_page_urls(browser):
    elems = browser.find_elements_by_css_selector(".job__tab.job__tab_top .job__item a.job__title")

    urls = []
    for elem in elems:
        urls.append(elem.get_attribute("href"))

    # only return 10 urls for test
    # return urls[:10]
    return urls

def _update_date_element_processor(element):
    raw_date = parser_helper.get_element_text(element)
    
    return parser_helper.format_to_date_string(raw_date, 
        src_format='%Y-%m-%d')

def create_run_config():

    return RunConfig(
        site_url=SITE_URL,
        field_selectors=CSS_SELECTORS,
        list_detail_page_urls_fn=_list_detail_page_urls,
        field_element_processors={
            'updated_date' : _update_date_element_processor})
