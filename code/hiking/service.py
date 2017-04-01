from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from hiking.core import Crawler

import threading
import logging

logger = logging.getLogger(__name__)

def start(run_configs, phantomjs_path=None, saver=None, log_saver=None, batch_size=5):
    logger.info('start crawling tasks with #%s configs ', len(run_configs))

    num_batches = int(len(run_configs)/batch_size) + 1

    logger.info('split #%s run configs to %s batch(size=%s)' % (len(run_configs), num_batches, batch_size))

    for i_batch in range(num_batches):
        min_ix = i_batch * batch_size
        max_ix = np.min([len(run_configs), ((i_batch+1) * batch_size)])

        run_configs_batch = run_configs[min_ix:max_ix]

        nloops = range(len(run_configs_batch))
        threads = []
        for i in nloops:
            crawler = Crawler(phantomjs_path=phantomjs_path)
            t = threading.Thread(target=crawler.start,
                args=(run_configs_batch[i](), saver, log_saver))
            threads.append(t)

        # start threads
        for i in nloops:
            threads[i].start()

        # wait for all threads to finish
        for i in nloops:
            threads[i].join()

    logger.info('ALL crawling tasks DONE')
