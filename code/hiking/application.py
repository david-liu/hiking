from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import logging

from hiking.devops import command_parameters_parser
from hiking.devops import setup_console_logging

import hiking.service as crawling_service

from hiking.repository import ConsoleRepository, EntityMongoRepository

logger = logging.getLogger(__name__)


class HikingApplication(object):
    def __init__(self, run_configs, repository=None, phantomjs_path=None):
        self._run_configs = run_configs
        self._repository = repository
        self._phantomjs_path = phantomjs_path

    def start(self):
        argv = sys.argv[1:]

        output_chanel, phantomjs_path, open_debug, db_name, collection_name = command_parameters_parser.get_running_options(argv)

        setup_console_logging(logging.DEBUG if open_debug else logging.INFO)

        logger.info("Start a Hiking application")
        
        
        if self._repository is None:
            if output_chanel == 'console':
                repo = ConsoleRepository()
            else:
                if db_name is None or collection_name is None:
                    print('For Mongodb output channel, you should specify the '
                        'database name and collection name through option: -d, '
                        'for example [-d db:collection], please try: code/app.py -h for help.\n')
                    sys.exit()

                repo = EntityMongoRepository(db_name=db_name, table_name=collection_name)
        else:
            repo = self._repository

        if self._phantomjs_path:
            phantomjs_path = self._phantomjs_path

        crawling_service.start(self._run_configs, phantomjs_path, repo.add_entity)