#! ENV/bin/python
### -*- coding: utf-8 -*-
#
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from hiking import HikingApplication

from run_configs.qiaobutang_top20 import create_run_config as qiaobutang_top20_run_config
from run_configs.shixiseng import create_run_config as shixiseng_run_config

if __name__ == "__main__":
    app = HikingApplication([shixiseng_run_config])

    app.start()