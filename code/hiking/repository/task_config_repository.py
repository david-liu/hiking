from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from sets import Set
import logging
import json
from hiking.utils import DBOperator
from hiking.core import run_config, CrawlingTask

logger = logging.getLogger(__name__)


class NextPageJumper(object):

    def __init__(self, next_page_css_selector, attribute_value_key='href', excluded_values=None, included_values=None):
        if excluded_values is None:
            self._excluded_values = []
        else:
            self._excluded_values = excluded_values

        if included_values is None:
            self._included_values = []
        else:
            self._included_values = included_values

        self._attribute_value_key = attribute_value_key
        self._next_page_links = Set()
        self._next_page_css_selector = next_page_css_selector

    def jump_to_next_page(self, browser):
        next_links = browser.find_elements_by_css_selector(
            self._next_page_css_selector)

        if len(next_links) == 0:
            return False

        for next_link in next_links:
            link_value = next_link.get_attribute(self._attribute_value_key)

            if ((not link_value) or
                    (link_value in self._next_page_links) or
                    (link_value in self._excluded_values) or
                    (self._included_values and link_value not in self._included_values)):
                continue
            else:
                self._next_page_links.add(link_value)

                next_link.click()

                return True

        return False


class TaskConfigurationRepository(object):

    def __init__(self, host='localhost', user='root', password='root', db='cfdb'):
        self.dbOperator = DBOperator(host=host,
                                     user=user,
                                     password=password,
                                     db=db)

    def get_crawling_task_config(self, crawling_task_ids):
        sql = "SELECT t.id, t.`type`, t.`url`, t.`save_type`, t.`saved_on`, t.`logged_on`, m.`crawler_channel_id`, m.block_selector, m.next_page_selector_config, m.`field_mapping` FROM crawler_task AS t, crawler_entity_mapping AS m WHERE t.entity_mapping_id = m.id AND t.id in (%s)" % ','.join(
            crawling_task_ids)

        task_definitions = self.dbOperator.list_by(sql, {})

        if not task_definitions:
            return None

        tasks = []
        for task_defintion in task_definitions:

            field_mapping = json.loads(task_defintion[u'field_mapping'])
            block_selector = task_defintion.get(u'block_selector')
            next_page_selector_config = task_defintion.get(
                u'next_page_selector_config')

            if not block_selector:
                block_selector = 'body'

            if next_page_selector_config:
                try:
                    next_page_selector_config = json.loads(
                        next_page_selector_config)

                    if 'css_selector' not in next_page_selector_config:
                        raise ValueError(
                            'css_selector is required for next_page_selector_config')

                    next_page_css_selector = next_page_selector_config[
                        u'css_selector']
                    attribute_value_key = 'href'
                    excluded_values = None
                    included_values = None

                    if 'attribute_value_key' in next_page_selector_config:
                        attribute_value_key = next_page_selector_config[
                            u'attribute_value_key']

                    if 'excluded_values' in next_page_selector_config:
                        excluded_values = next_page_selector_config[
                            u'excluded_values']

                    if 'included_values' in next_page_selector_config:
                        included_values = next_page_selector_config[
                            u'included_values']

                    page_jumper = NextPageJumper(next_page_css_selector,
                                                 attribute_value_key=attribute_value_key,
                                                 excluded_values=excluded_values,
                                                 included_values=included_values)

                except Exception as e:
                    page_jumper = NextPageJumper(next_page_selector_config)

                next_page_jump_fn = page_jumper.jump_to_next_page
            else:
                next_page_jump_fn = None


            print(task_defintion[u'url'])   
             
            field_mappings = run_config.RunConfig(site_url=task_defintion[u'url'],
                                                  field_selectors=field_mapping,
                                                  config_id=task_defintion[
                                                      u'id'],
                                                  block_selector=block_selector,
                                                  in_page_jumping_fn=next_page_jump_fn)

            tasks.append(CrawlingTask(
                task_id=task_defintion[u'id'],
                channel_id=task_defintion[u'crawler_channel_id'],
                saved_on_url=task_defintion[u'saved_on'],
                logged_on_url=task_defintion[u'logged_on'],
                run_config=field_mappings))

        return tasks
