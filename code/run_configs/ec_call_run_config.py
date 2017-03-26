### -*- coding: utf-8 -*- 
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
from hiking.utils import parser_helper, url_helper, file_io_helper
from hiking.core.run_config import ByKeys, FieldTypeKeys, FieldMultiplicityKeys, RunConfig


CSS_SELECTORS = {
    "title" :  {
        'key' : '.title_word',
        'is_primary' : True
    },
    "summary" : '.s_r_summ',
    'detail_url' : 'table h2.s_r_title > a'
}

def _list_detail_page_urls(browser):
    return []

def in_page_jumping_fn(browser):
    next_links =  browser.find_elements_by_css_selector(".grayr a")

    if len(next_links) == 0:
        return False

    if next_links[-1].text.strip()==u'下一页':
        next_links[-1].click();
        return True
    else:
        return False

def _datails_page_element_processor(element):
    url = parser_helper.get_element_attribute(element, 'href')
    return url

def create_run_config(urls):
    return RunConfig(
            site_url=urls,
            field_selectors=CSS_SELECTORS,
            list_detail_page_urls_fn=_list_detail_page_urls,
            field_element_processors={
                'detail_url' : _datails_page_element_processor})

def create_batch_run_config(urls, max_num_thread = 50):
    if len(urls) < max_num_thread:
        max_num_thread = len(urls)

    batch_size = int(len(urls) / max_num_thread)

    fun_configs = []
    for i in range(max_num_thread):
        start = batch_size * i
        end = batch_size * (i + 1)

        if end > len(urls):
            end = len(urls)

        batch_urls = urls[start:end]

        fun_config = functools.partial(
            create_run_config,
            urls=batch_urls)
        fun_configs.append(fun_config)

    return fun_configs
