#! ENV/bin/python
### -*- coding: utf-8 -*-
#
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from hiking import HikingApplication

from run_configs.iwencai_news import create_run_config as iwencai_news_run_config

if __name__ == "__main__":
    app = HikingApplication([iwencai_news_run_config])

    app.start()