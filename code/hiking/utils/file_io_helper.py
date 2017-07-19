from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import codecs
import gzip
import logging
import functools


logger = logging.getLogger(__name__)

class FileReadVisits(object):
	"""A File Lines's container

	   the class can iterator over the specied file.
	"""
	def __init__(self, data_path):
		self.data_path = data_path

	def __iter__(self):
		fopen = gzip.open if self.data_path.endswith(".gz") else functools.partial(codecs.open, encoding='utf-8')

		with fopen(self.data_path) as fin:
			for line in fin:
				yield line


def create_file_iter(path, line_decoder=None, max_lines = None, skipped_header_lines = 0):
    """ Create a line iterator for a specified file

    Returns an iterator over the specified path, the format of the file follows

    Args:
        path: the the path of the corpus file
        line_decoder: the decoder to process the line
        max_lines: the maxium line to read
        skipped_header_lines: the lines to skip from the first line of the file

    Returns:
    	a iterator of file line, which decoded with the linedecoder 
    """

    visits = FileReadVisits(path)

    total_lines = 1
    cnt = 0
    for line in visits:
        cnt += 1
        if cnt <= skipped_header_lines:
        	continue

        if len(line.strip()) == 0:
            continue

        result = line if line_decoder is None else line_decoder(line)

        if result is not None:
            if max_lines is not None and total_lines > max_lines:
                break
            total_lines += 1

            yield result