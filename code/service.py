
import threading
from time import sleep, ctime
from core.job_crawler import JobCrawler
from parsers.qiaobutang_top20 import QiaobutangSiteTop20Parser
from parsers.shixiseng import ShixisengSiteParser
from repository.job_console_repository import JobConsoleRepository
from repository.job_mongo_repository import JobMongoRepository


def crawling_qiaobutang(crawler, save_fn):
	parser = QiaobutangSiteTop20Parser()
	crawler.start(parser, save_fn)

def crawling_shixiseng(crawler, save_fn):
	parser = ShixisengSiteParser()
	crawler.start(parser, save_fn)

crawling_tasks = [crawling_qiaobutang, crawling_shixiseng]

def main():
	print('start at: %s' % ctime())
	crawler = JobCrawler()
	repo = JobMongoRepository()
	#repo = JobConsoleRepository()
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

