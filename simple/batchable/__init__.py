from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor


class BatchableCrawlerProcess(CrawlerProcess):

    """
    A CrawlerProcess that batches .crawl() requests to keep the
    scrapy stack happy. Use when you have to call .crawl() in excess
    of 100s to 1000s.

    Purpose:

            Batch up an arbitrary number of crawlers over any length
            of time. The reactor will be started once and kept running
            until you call stop.

    Why?

            This was implemented to fix a erronuous behavior in Scrapy: When
            large batches of .crawl() requets are submitted to a 
            CrawlerProcess() it may cause DNSLookupError and 
            Resource temporarily unavailable errors. 

            Batching up requests as shown below avoids this. 

    Usage:
        # create process
        process = BatchableCrawlerProcess()
        process.start(autobatch=True, batchsize=100) # non-blocking
        # batch up crawlers
        for batch in batches:
            process.crawl('spider', **kwargs)
        # once all is done
        process.stop()

        If you want to have more control over batching:

        process.start(autobatch=False)
        for batch in batches:
            process.crawl(...)
            if some_condition:
                # wait until no more crawlers are active
                process.join()
        process.stop()
    """

    def __init__(self, autobatch=True, settings=None,
                 batchsize=100, **kwargs):
        super(CrawlerProcess, self).__init__(settings=settings, **kwargs)
        self._reactor = None
        self.autobatch = autobatch
        self.batchsize = batchsize

    def crawl(self, crawler_or_spidercls, join_callback=None, *args, **kwargs):
        """
        crawl a spider, batching calls before accepting new ones

        if the currently active number of crawlers exceeds self.batchsize
        will wait until all have completed before proceeding. this helps
        to avoid the crawler process from overflodding with requests and
        keeps it healthy.  
        """
        if self.autobatch and len(self._active) > self.batchsize:
            self.join()
            if join_callback:
                join_callback()
        return super(BatchableCrawlerProcess, self).crawl(crawler_or_spidercls, *args, **kwargs)

    def start(self):
        """
        starts the reactor and keeps it running until stop() is called



        Essentially the same as adopted from CrawlerProcess.start() but
        does not block and does not automatically stop the reactor once
        all crawlers are done. 
        """
        if self._reactor is None:
            reactor.installResolver(self._get_dns_resolver())
            self.reactor = tp = reactor.getThreadPool()
            tp.adjustPoolsize(
                maxthreads=self.settings.getint('REACTOR_THREADPOOL_MAXSIZE'))
            reactor.addSystemEventTrigger('before', 'shutdown', self.stop)
        reactor.startRunning(False)

    def _stop_reactor(self, _=None):
        pass

    def stop(self):
        super(BatchableCrawlerProcess, self).stop()
        super(BatchableCrawlerProcess, self)._stop_reactor()
