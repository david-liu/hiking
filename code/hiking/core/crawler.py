from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import platform
import time
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import types

from hiking.core.run_config import ByKeys, FieldTypeKeys, FieldMultiplicityKeys
from hiking.utils import parser_helper


logger = logging.getLogger(__name__)


class Crawler(object):

    def __init__(self, phantomjs_path=None):
        self._phantomjs_path = phantomjs_path

    def start(self, run_config, save_fn=None):
        return self._crawling_page(url=run_config.site_url,
                                   list_detail_page_urls_fn=run_config.list_detail_page_urls_fn,
                                   field_selectors=run_config.field_selectors,
                                   block_selector=run_config.block_selector,
                                   run_config_id=run_config.config_id,
                                   in_page_jumping_fn=run_config.in_page_jumping_fn,
                                   field_element_processors=run_config.field_element_processors,
                                   field_value_processors=run_config.field_value_processors,
                                   primary_fields=run_config.primary_fields,
                                   save_fn=save_fn)

    def _crawling_page(self, url, list_detail_page_urls_fn, field_selectors, run_config_id=None, primary_fields=None, block_selector="body", in_page_jumping_fn=None, field_element_processors=None, field_value_processors=None, save_fn=None):
        if not isinstance(url, list):
            urls = [url]
        else:
            urls = url

        if in_page_jumping_fn is None:
            in_page_jumping_fn = lambda x: False

        if primary_fields is None:
            primary_fields = ['url']

        objects = []

        if self._phantomjs_path is not None:
            browser = webdriver.PhantomJS(self._phantomjs_path)
        else:
            browser = webdriver.Chrome()

        for url in urls:

            try:
                logger.info("begin to crawl from: %s", url)

                browser.get(url)

                time.sleep(5)

                if list_detail_page_urls_fn is None:
                    urls = [url]
                else:
                    urls = list_detail_page_urls_fn(browser)

                    if (isinstance(urls, list) or isinstance(urls, dict)) and len(urls) == 0:
                        logger.log("Can not find any detials urls in: %s", url)

                if (isinstance(urls, list) or isinstance(urls, dict)):
                    logger.info("find #%s details links in: %s" %
                                (len(urls), url))
                else:
                    logger.info("find geneartor details links in: %s" % (url))

                if isinstance(urls, dict):
                    iterateItems = urls.items()
                elif isinstance(urls, list):
                    iterateItems = enumerate(urls)

                for key, url in iterateItems:

                    while True:
                        blocks = browser.find_elements_by_css_selector(
                            block_selector)

                        logger.debug("find #%s blocks areas in [%s] with css selector [%s]" % (
                            len(blocks), url, block_selector))

                        for block in blocks:
                            obj = self.__parse_block_detail_page(
                                root_element=block,
                                url=browser.current_url,
                                field_selectors=field_selectors,
                                field_element_processors=field_element_processors,
                                field_value_processors=field_value_processors)

                            if isinstance(urls, dict):
                                obj['query_key'] = key

                            if save_fn is not None:
                                save_fn(
                                    obj, primary_fields, run_config_id=run_config_id)

                            objects.append(obj)

                        has_more_in_page = in_page_jumping_fn(browser)

                        if not has_more_in_page:
                            break
                        else:
                            time.sleep(2)

            except Exception as inst:
                logger.error("Find exception during Crawling page: %s", inst)
            finally:
                pass

        browser.quit()

        return objects

    def __parse_block_detail_page(self, root_element, url, field_selectors, field_element_processors=None, field_value_processors=None):

        field_element_processors = {} if field_element_processors is None else field_element_processors
        field_value_processors = {} if field_value_processors is None else field_value_processors

        obj = {}
        obj["_url"] = url

        for (field_name, field_selector) in field_selectors.items():
            try:
                if not field_selectors or not field_selector.key:
                    obj[field_name] = None
                    continue

                field_element_processor = field_element_processors.get(
                    field_name)
                field_value_processor = field_value_processors.get(field_name)

                field_value = self.__parse_field_content(root_element=root_element,
                                                         field_name=field_name,
                                                         field_selector=field_selector,
                                                         element_text_processor=field_element_processor,
                                                         field_value_processor=field_value_processor)

                obj[field_name] = field_value
            except Exception as inst:
                logger.error(
                    "Find exception during Crawling page: %s", field_name)

        return obj

    def __parse_field_content(self, root_element, field_name, field_selector, element_text_processor=None, field_value_processor=None):

        element_text_processor = parser_helper.get_element_text if element_text_processor is None else element_text_processor

        elements = []
        if field_selector.by == ByKeys.CSS_SELECTOR:
            elements = root_element.find_elements_by_css_selector(
                field_selector.key)
        elif field_selector.by == ByKeys.ID:
            elements = []
            try:
                element = [root_element.find_element_by_id(field_selector.key)]
                elements.append[element]
            except NoSuchElementException as e:
                pass
        elif field_selector.by == ByKeys.NAME:
            elements = root_element.find_elements_by_name(field_selector.key)
        elif field_selector.by == ByKeys.CLASS_NAME:
            elements = root_element.find_elements_by_class_name(
                field_selector.key)
        elif field_selector.by == ByKeys.X_PATH:
            elements = root_element.find_elements_by_xpath(field_selector.key)

        if len(elements) == 0:
            logger.error("can not find field [%s] with [%s] selector: [%s] in: %s, set [None] value for this field",
                         field_name, field_selector.key, field_selector.by, browser.current_url)
            value = None

        elif field_selector.multi == FieldMultiplicityKeys.ONE:
            value = element_text_processor(elements[0])
        else:
            value = [element_text_processor(element) for element in elements]

        if field_value_processor:
            value = field_value_processor(value)

        if field_selector.value_type == FieldTypeKeys.DATE:
            value = parser_helper.format_to_date(
                value, src_format=field_selector.value_format)

        return value
