import os
import sys
import platform
import time
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from hiking.core.run_config import ByKeys, FieldTypeKeys, FieldMultiplicityKeys
import hiking.utils.webelement_parser_helper as parser_helper


logger = logging.getLogger(__name__)

class Crawler(object):

    def __init__(self, phantomjs_path=None):
        self._phantomjs_path = phantomjs_path

    def start(self, run_config, save_fn=None):
        return self._crawling_page(url=run_config.site_url, 
            list_detail_page_urls_fn=run_config.list_detail_page_urls_fn,
            field_selectors=run_config.field_selectors,
            field_element_processors=run_config.field_element_processors,
            save_fn=save_fn)


    def _crawling_page(self, url, list_detail_page_urls_fn, field_selectors, field_element_processors = None, save_fn=None):
        
        objects = []
        try:
            logger.info("begin to crawl from: %s", url)
            if self._phantomjs_path is not None:
                browser = webdriver.PhantomJS(self._phantomjs_path)
            else:
                browser = webdriver.Firefox()

            browser.get(url)
            urls = list_detail_page_urls_fn(browser)

            if len(urls) == 0:
                logger.error("Can not find any detials urls in: %s", url)
            else:
                logger.info("find #%s details links in: %s" % (len(urls), url))
                for url in urls:
                    obj = self.__parse_job_detail_page(
                        browser, 
                        url, 
                        field_selectors, 
                        field_element_processors)

                    if save_fn is not None:
                        save_fn(obj)

                    objects.append(obj)

        except Exception as inst:
            logger.error("Find exception during Crawling page: %s" , inst)
        finally:
            browser.quit()

        return objects


    def __parse_job_detail_page(self, browser, url, field_selectors, field_element_processors = None):
        browser.get(url)
        
        field_element_processors = {} if field_element_processors is None else field_element_processors
        obj = {}
        obj["url"] = url
        for (field_name, field_selector) in field_selectors.items():
            if not field_selectors or not field_selector.key:
                obj[field_name] =  None
                continue
                
            field_element_processor = field_element_processors.get(field_name)

            field_value = self.__parse_field_content(browser, field_name, field_selector, field_element_processor)
            obj[field_name] = field_value

        return obj

    def __parse_field_content(self, browser, field_name, field_selector, element_text_processor=None):
        
        element_text_processor  = parser_helper.get_element_text if element_text_processor is None else element_text_processor

        elements = []
        if field_selector.by == ByKeys.CSS_SELECTOR:
            elements = browser.find_elements_by_css_selector(field_selector.key)
        elif field_selector.by == ByKeys.ID:
            elements = []
            try:
                element = [browser.find_element_by_id(field_selector.key)]
                elements.append[element]
            except NoSuchElementException as e:
                pass
        elif field_selector.by == ByKeys.NAME:
            elements = browser.find_elements_by_name(field_selector.key)
        elif field_selector.by == ByKeys.CLASS_NAME:
            elements = browser.find_elements_by_class_name(field_selector.key)
        elif field_selector.by == ByKeys.X_PATH:
            elements = browser.find_elements_by_xpath(field_selector.key)

        if len(elements) == 0:
            logger.error("can not find field [%s] with [%s] selector: [%s] in: %s, set [None] value for this field", field_name, field_selector.key, field_selector.by, browser.current_url)
            value = None
        
        elif field_selector.multi == FieldMultiplicityKeys.ONE:
            value =  element_text_processor(elements[0])
        else:
            value = [element_text_processor(element) for element in elements]

            
        return value

