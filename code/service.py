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


run_configs = [qiaobutang_top20_run_config, shixiseng_run_config]

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
                print ("Job chrawler version: 0.0.1")
                print ("usage: code/service.py")
                print ("Options:")
                print ("   %-30s%s" % ("-o [ --output ]", "channel to save the crawling results, the output channel can be:"))
                print ("   %-30s  %-10s%s" % ("", "console", "print the result in cosole"))
                print ("   %-30s  %-10s%s" % ("", "mongodb", "save the result to the mongodb database"))
                print ("   %-30s%s" % ("", "and the default channel is [console]"))
                
                print ("   %-30s%s" % ("-h [ --help ]", "show this usage information"))
                
                
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
    
    if output_chanel == 'console':
        repo = JobConsoleRepository()
    else:
        repo = JobMongoRepository()

    nloops = range(len(run_configs))
    threads = []
    for i in nloops:
        crawler = JobCrawler()
        t = threading.Thread(target=crawler.start,
            args=(run_configs[i](), repo.add_job))
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

