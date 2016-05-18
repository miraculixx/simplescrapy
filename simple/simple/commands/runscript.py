from importlib import import_module
import os
import pydoc
import sys

from scrapy.commands import ScrapyCommand
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import UsageError


class Command(ScrapyCommand):

    """
    show help on spider
    """
    requires_project = True

    def add_options(self, parser):
        super(Command, self).add_options(parser)
        parser.add_option('-n', "--calls", default=10)

    def syntax(self):
        return "<spider>"

    def short_desc(self):
        return "Run a scrapy script"

    def long_desc(self):
        return "Run a scripy script"

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
            process = CrawlerProcess(settings=get_project_settings())
            scriptmod.run(process, calls=calls)
