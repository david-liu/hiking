#! ENV/bin/python
### -*- coding: utf-8 -*-
#
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import numpy as np
from hiking import HikingApplication
from hiking.utils import parser_helper, url_helper, file_io_helper

from run_configs.ec_call_run_config import create_batch_run_config


def ec_call_line_decoder(line):
    if len(line.strip()) == 0:
        return None

    crm_id,user_id,duration,record_url = line.strip().split(",")



    return record_url

if __name__ == "__main__":

    file_iter = file_io_helper.create_file_iter(
            path="data/crm_outbound-record_1000_v3.csv",
            line_decoder=ec_call_line_decoder,
            max_lines = 20,
            skipped_header_lines = 1)

    urls = []
    for url in file_iter:
        urls.append(url)

    urls =np.random.permutation(urls)

    app = HikingApplication(create_batch_run_config(urls, 20))

    app.start()
