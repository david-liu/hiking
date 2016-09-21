
import threading
from time import sleep, ctime
from core.job_crawler import JobCrawler
from parsers.qiaobutang import QiaobutangSiteParser
from parsers.shixiseng import ShixisengSiteParser
from repository.job_console_repository import JobConsoleRepostory
from repository.job_mongo_repository import JobMongoRepostory


def crawling_qiaobutang(crawler, save_fn):
	parser = QiaobutangSiteParser()
	crawler.start(parser, save_fn)

def crawling_shixiseng(crawler, save_fn):
	parser = ShixisengSiteParser()
	crawler.start(parser, save_fn)

crawling_tasks = [crawling_qiaobutang, crawling_shixiseng]

def main():
	print('start at: %s' % ctime())
	crawler = JobCrawler()
	repo = JobMongoRepostory()
	#repo = JobConsoleRepostory()
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

	print('ALL crawling tasks DONE at: %s' % ctime())

if __name__ == "__main__":
	main()

