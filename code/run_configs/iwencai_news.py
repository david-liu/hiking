### -*- coding: utf-8 -*- 
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from hiking.utils import parser_helper, url_helper
from hiking.core.run_config import ByKeys, FieldTypeKeys, FieldMultiplicityKeys, RunConfig

SITE_URL = 'http://www.iwencai.com/'

keywords = [u"半年报", u"定向增发", u"董事会决议", u"非公开发行", u"风险警示", u"复牌", u"股东大会", u"股权激励", u"季报", u"年报", u"首次公开发行", u"停牌", u"退市", u"异常波动", u"员工持股", u"增发", u"资产重组", u"违法", u"IPO", u"招股", u"违规", u"违纪", u"犯罪"]

CSS_SELECTORS = {
    "title" :  '.title_word',
    "summary" : '.s_r_summ'
}

def _list_detail_page_urls(browser):
    base_url = 'http://www.iwencai.com/search?typed=0&preParams=&ts=1&f=1&qs=result_tab&selfsectsn=&querytype=&bgid=&sdate=&edate=&searchfilter=&tid=news'

    urls = {}
    for keyword in keywords:
        url = url_helper.build_url(base_url, {'w': keyword})
        urls[keyword] = url

    return urls

def in_page_jumping_fn(browser):
    next_links =  browser.find_elements_by_css_selector(".grayr a")

    if len(next_links) == 0:
        return False

    if next_links[-1].text.strip()==u'下一页':
        next_links[-1].click();
        return True
    else:
        return False

def create_run_config():
    
    return RunConfig(
        site_url=SITE_URL,
        field_selectors=CSS_SELECTORS,
        list_detail_page_urls_fn=_list_detail_page_urls,
        block_selector='.s_r_box',
        in_page_jumping_fn=in_page_jumping_fn)
