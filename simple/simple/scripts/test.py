from scrapy.crawler import CrawlerProcess


def run(crawler, calls=None, **kwargs):
    ":type crawler: BatchableCrawlerProcess"
    total = int(calls) or 10
    for i in range(0, total):
        if i > 0 and i % (total * .1) == 0 or i == total - 1:
            print "Started %s crawlers" % i
        crawler.crawl('test')
    if type(crawler) == CrawlerProcess:
        print "now starting crawlers... this will fail if -n > 1500"
        crawler.start()
    print "done."
