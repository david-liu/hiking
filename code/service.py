#! ENV/bin/python
### -*- coding: utf-8 -*- 

import threading
from time import sleep, ctime
import sys, getopt

import utils.log_helper as logger
from core.job_crawler import JobCrawler
from configs.qiaobutang_top20 import create_run_config as qiaobutang_top20_run_config
from configs.shixiseng import create_run_config as shixiseng_run_config

from repository.job_console_repository import JobConsoleRepository
from repository.job_mongo_repository import JobMongoRepository


def crawling_qiaobutang(crawler, save_fn):
	config = qiaobutang_top20_run_config()

	crawler.start(config, save_fn)

def crawling_shixiseng(crawler, save_fn):
	config = shixiseng_run_config()

	crawler.start(config, save_fn)

crawling_tasks = [crawling_qiaobutang, crawling_shixiseng]

def get_output_channel(argv):

    output_chanel = "console"
    if len(argv) > 0:
        try:
            opts, args = getopt.getopt(argv,"ho:",["output="])
        except getopt.GetoptError:
            print('Invalid arguments, please try: code/service.py -h for help\n')
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print ("code/service.py -o [output channel]\n")
                print ("The support output channel includes: console|mongodb\n")
                sys.exit()
            
            if opt in ("-o", "--output"):
                if arg not in ("console", "mongodb"):
                    print ("Invalid output channel: [%s], please try: code/service.py -h for help\n" % arg)
                    sys.exit()
                output_chanel = arg

    return output_chanel

def main(argv):
    output_chanel = get_output_channel(argv)

    logger.info('start at: %s', ctime())
    crawler = JobCrawler()

    if output_chanel == 'console':
        repo = JobConsoleRepository()
    else:
        repo = JobMongoRepository()

    nloops = range(len(crawling_tasks))
    threads = []
    for i in nloops:
        t = threading.Thread(target=crawling_tasks[i],
            args=(crawler, repo.add_job))
        threads.append(t)

    # start threads
    for i in nloops:
        threads[i].start()

    # wait for all threads to finish
    for i in nloops:
        threads[i].join()

    logger.info('ALL crawling tasks DONE at: %s' % ctime())


if __name__ == "__main__":
    main(sys.argv[1:])

