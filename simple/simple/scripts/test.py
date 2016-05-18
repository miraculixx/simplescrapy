

def run(crawler, calls=None, **kwargs):
    # works up to total approx 1000
    # fails from total 1500 onwards
    total = int(calls) or 10
    for i in range(0, total):
        if i > 50 and i % (total * .1) == 0 or i == total - 1:
            print "Started %s crawlers" % i
        crawler.crawl('test')
    print "Starting actual crawl..."
    crawler.start()
    print "done."