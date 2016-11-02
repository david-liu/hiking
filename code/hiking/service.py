from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from hiking.core import Crawler

import threading
import logging

logger = logging.getLogger(__name__)


def start(run_configs, phantomjs_path=None, saver=None):
    logger.info('start crawling tasks with #%s configs ', len(run_configs))

    nloops = range(len(run_configs))
    threads = []
    for i in nloops:
        crawler = Crawler(phantomjs_path=phantomjs_path)
        t = threading.Thread(target=crawler.start,
            args=(run_configs[i](), saver))
        threads.append(t)

    # start threads
    for i in nloops:
        threads[i].start()

    # wait for all threads to finish
    for i in nloops:
        threads[i].join()

    logger.info('ALL crawling tasks DONE')
