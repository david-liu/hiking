from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys, getopt
import logging


def usage():
    print ("Job chrawler version: 0.0.1")
    print ("usage: code/app.py")
    print ("Options:")
    print ("   %-30s%s" % ("-o,--output <args>", "Set channel to print the crawling results, the output channel can be:"))
    print ("   %-30s  %-10s%s" % ("", "console", "Print the result in cosole"))
    print ("   %-30s  %-10s%s" % ("", "mongodb", "Save the result to the mongodb database"))
    print ("   %-30s%s" % ("", "and the default channel is [console]"))
    print ("   %-30s%s" % ("-d,--db", "Specify the database and collection when the output channel is mongodb. usage: database:collection"))
    print ("   %-30s%s" % ("--headless <args>", "Set path of the phantomjs excutable file"))
    print ("   %-30s%s" % ("-X,--debug", "Produce execution debug output"))
    print ("   %-30s%s" % ("-h,--help", "Show this usage information"))


def get_running_options(argv):

    output_chanel = "console"
    db_name = None
    collection_name = None
    phantomjs_path = None
    open_debug = False
    if len(argv) > 0:
        try:
            opts, args = getopt.getopt(argv,"hXo:d:",["output=", "db=", "headless=", "debug"])
        except getopt.GetoptError:
            print('Invalid arguments, please try: -h for help\n')
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()

                sys.exit()

            if opt in ("-X", "--debug"):
                open_debug = True

            if opt in ("-o", "--output"):
                if arg not in ("console", "mongodb"):
                    print ("Invalid output channel: [%s], please try:  -h for help\n" % arg)
                    sys.exit()

                output_chanel = arg

            if opt in ("-d", "--db"):
                parts = arg.split(':')
                if len(parts) != 2:
                    print ("Invalid data source: [%s], please try:  -h for help\n" % arg)
                    sys.exit()

                db_name = parts[0]
                collection_name = parts[1]

            if opt  == "--headless":
                if not os.path.exists(arg):
                    print ("The phantomsjs file  for [%s] did not exit, please check it ", arg)
                    sys.exit()

                phantomjs_path = arg

    return (output_chanel, phantomjs_path, open_debug, db_name, collection_name)