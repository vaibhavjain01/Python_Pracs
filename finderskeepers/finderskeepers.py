import crawler
import logger

class finderskeepers:
    finderskeepers_crawler = crawler.generic_url_crawler(7, 'https://www.udacity.com/cs101x/index.html')
    finderskeepers_logger = logger.generic_python_logger(7)
    
    def __init__(self):
        self.finderskeepers_logger.GENERIC_PYTHON_LOGGER_LOG(self.finderskeepers_logger.LOGGER_LOG_LEVEL_TRACE, "Sequence Initiated")
        self.finderskeepers_crawler.crawler_crawl()


check_finderskeepers = finderskeepers()