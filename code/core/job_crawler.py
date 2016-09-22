from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import utils.log_helper as logger

class JobCrawler(object):

    def start(self, run_config, save_fn=None):
        return self._crawling_page(url=run_config.site_url, 
            list_detail_page_urls_fn=run_config.list_detail_page_urls_fn,
            field_css_selectors=run_config.field_css_selectors,
            field_element_processors=run_config.field_element_processors,
            save_fn=save_fn)


    def _crawling_page(self, url, list_detail_page_urls_fn, field_css_selectors, field_element_processors = None, save_fn=None):
        
        jobs = []
        try:
            logger.info("begin to crawl jobs from: %s", url)
            browser = webdriver.Firefox()
            browser.get(url)
            urls = list_detail_page_urls_fn(browser)

            if len(urls) == 0:
                logger.error("Can not find any detials urls in: %s", url)
            else:
                logger.debug("find #%s details pages in: %s" % (len(urls), url))
                for url in urls:
                    job = self.__parse_job_detail_page(
                        browser, 
                        url, 
                        field_css_selectors, 
                        field_element_processors)

                    if save_fn is not None:
                        save_fn(job)

                    jobs.append(job)

        except Exception as inst:
            logger.error("Find exception during Crawling page: %s" , inst)
        finally:
            browser.quit()

        return jobs


    def __parse_job_detail_page(self, browser, url, field_css_selectors, field_element_processors = None):
        browser.get(url)

        job = {}
        job["url"] = url
        for (name, css_selector) in field_css_selectors.items():
            if not css_selector:
                job[name] =  None
                continue
                
            field_element_processor = None
            if field_element_processors is not None and name in field_element_processors:
                field_element_processor = field_element_processors[name]

            value = self.__parse_field_content(browser, name, css_selector, field_element_processor)
            job[name] = value

        return job

    def __parse_field_content(self, browser, field_name, field_css_selector, element_text_processor=None):
        try:
            element = browser.find_element_by_css_selector(field_css_selector)
        except NoSuchElementException as inst:
            logger.error("can not find field [%s] with css selector: [%s] in: %s, with [None] value for this fild", field_name, field_css_selector, browser.current_url)
            return None
        else:
            if element_text_processor is None:
                element_text_processor = lambda e : e.text

            return element_text_processor(element)