from importlib import import_module
import os
import pydoc
import sys

from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError

from batchable import BatchableCrawlerProcess
from scrapy.crawler import CrawlerProcess


class Command(ScrapyCommand):

    """
    show help on spider
    """
    requires_project = True

    def add_options(self, parser):
        super(Command, self).add_options(parser)
        parser.add_option('-n', "--calls", default=10)
        parser.add_option('-X', "--use-standard-failing-process",
                          action='store_true', default=False)
    def syntax(self):
        return "<spider>"

    def short_desc(self):
        return "Run a scrapy script"

    def long_desc(self):
        doc = """Run a scrapy script
        
        Scrapy scripts are python modules that live in a project's
        .scripts package and expose a run() method. 
        
        The run() method receives a crawler process instance that is 
        already started and is ready to receive 
        .crawl('spider', *args, **kwargs) calls.
        
        To wait for crawlers to complete, call .join(). 
        """

    def _err(self, msg):
        sys.stderr.write(msg + os.linesep)
        self.exitcode = 1

    def run(self, args, opts):
        if len(args) < 1:
            raise UsageError()

        script = args[0]
        calls = opts.calls

        try:
            scriptmod = import_module('.scripts.%s' % script, 'simple')
        except:
            raise
        else:
            from scrapy.utils.project import get_project_settings
            if not opts.use_standard_failing_process:
                process = BatchableCrawlerProcess(
                    settings=get_project_settings())
                process.start()
                scriptmod.run(process, calls=calls)
                process.stop()
            else:
                print "WARNING - this will fail!"
                process = CrawlerProcess(
                    settings=get_project_settings())
                scriptmod.run(process, calls=calls)