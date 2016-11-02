#! ENV/bin/python
### -*- coding: utf-8 -*-

import os
import sys, getopt
import logging

import hiking.service as crawling_service

from hiking.repository.job_console_repository import JobConsoleRepository
from hiking.repository.job_mongo_repository import JobMongoRepository
from hiking.devops.cmdline import setup_console_logging

from run_configs.qiaobutang_top20 import create_run_config as qiaobutang_top20_run_config
from run_configs.shixiseng import create_run_config as shixiseng_run_config

logger = logging.getLogger(__name__)

#run_configs = [qiaobutang_top20_run_config, shixiseng_run_config]

run_configs = [shixiseng_run_config]

def usage():
    print ("Job chrawler version: 0.0.1")
    print ("usage: code/app.py")
    print ("Options:")
    print ("   %-30s%s" % ("-o,--output <args>", "set channel to print the crawling results, the output channel can be:"))
    print ("   %-30s  %-10s%s" % ("", "console", "print the result in cosole"))
    print ("   %-30s  %-10s%s" % ("", "mongodb", "save the result to the mongodb database"))
    print ("   %-30s%s" % ("", "and the default channel is [console]"))
    print ("   %-30s%s" % ("--headless <args>", "Set path of the phantomjs excutable file"))
    print ("   %-30s%s" % ("-X,--debug", "Produce execution debug output"))
    print ("   %-30s%s" % ("-h,--help", "show this usage information"))


def get_running_options(argv):

    output_chanel = "console"
    phantomjs_path = None
    open_debug = False
    if len(argv) > 0:
        try:
            opts, args = getopt.getopt(argv,"hXo:",["output=", "headless=", "debug"])
        except getopt.GetoptError:
            print('Invalid arguments, please try: code/app.py -h for help\n')
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()

                sys.exit()

            if opt in ("-X", "--debug"):
                open_debug = True

            if opt in ("-o", "--output"):
                if arg not in ("console", "mongodb"):
                    print ("Invalid output channel: [%s], please try: code/app.py -h for help\n" % arg)
                    sys.exit()
                output_chanel = arg

            if opt  == "--headless":
                if not os.path.exists(arg):
                    print ("The phantomsjs file  for [%s] did not exit, please check it ", arg)
                    sys.exit()

                phantomjs_path = arg

    return (output_chanel, phantomjs_path, open_debug)


def main(argv):
    output_chanel, phantomjs_path, open_debug = get_running_options(argv)

    setup_console_logging(logging.DEBUG if open_debug else logging.INFO)
    
    if output_chanel == 'console':
        repo = JobConsoleRepository()
    else:
        repo = JobMongoRepository()

    crawling_service.start(run_configs,phantomjs_path, repo.add_job)

if __name__ == "__main__":
    main(sys.argv[1:])
