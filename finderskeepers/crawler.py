# ##########################################################################################
#                                        IMPORTS
# ##########################################################################################

import urllib.request
import logger


# Crawler
class generic_url_crawler:
    
    crawler_seed = ''
    crawler_log_level = 0

    # Some Typical Macros in form of global variables
    CRAWLER_ERROR = -1
    CRAWLER_SUCCESS = 1
    CRAWLER_FOUND = CRAWLER_SUCCESS
    CRAWLER_NOT_FOUND = CRAWLER_ERROR
    CRAWLER_TRUE = CRAWLER_SUCCESS
    CRAWLER_FALSE = CRAWLER_ERROR

    # The two lists, to track the pages to be crawled and already crawled
    crawler_to_crawl = []
    crawler_crawled = []

    # Logger class object
    crawler_logger = None

    # Constructor
    def __init__(self, crawler_log_level_in, crawler_seed_in):
        self.crawler_log_level = crawler_log_level_in
        self.crawler_seed = crawler_seed_in
        self.crawler_to_crawl.append(crawler_seed_in)
        self.crawler_logger = logger.generic_python_logger(self.crawler_log_level)
        
    # Function to get HTML Resources from url
    def crawler_get_html_res(self, crawler_input_page):
    
        self.crawler_logger.GENERIC_PYTHON_LOGGER_LOG (self.crawler_logger.LOGGER_LOG_LEVEL_TRACE, "crawler_get_html_res: Getting links from url " + crawler_input_page)
        with urllib.request.urlopen(crawler_input_page, None, 3) as response:
            crawler_local_read_html = response.read()
            self.crawler_update_url_index_db(self.crawler_to_crawl, 'delete', crawler_input_page)
            self.crawler_update_url_index_db(self.crawler_crawled, 'add', crawler_input_page)
            return (crawler_local_read_html)
    
    
    # Function to update the crawler lists with appropriate function, at provided index (url)
    def crawler_update_url_index_db(self, crawler_list_name, crawler_list_function, crawler_update_input_url):
        if(crawler_list_function == 'add'):
            crawler_list_name.append(crawler_update_input_url)
            if(crawler_list_name == self.crawler_crawled):
                self.crawler_logger.GENERIC_PYTHON_LOGGER_LOG(self.crawler_logger.LOGGER_LOG_LEVEL_ERROR, "crawler_update_url_index_db: Add Success for " + crawler_update_input_url + " to crawler_crawled")
            else:
                self.crawler_logger.GENERIC_PYTHON_LOGGER_LOG(self.crawler_logger.LOGGER_LOG_LEVEL_ERROR, "crawler_update_url_index_db: Add Success for " + crawler_update_input_url + " to crawler_to_crawl")
                
        if(crawler_list_function == 'delete'):
            try:
                crawler_list_name.remove(crawler_update_input_url)
            except ValueError:
                self.crawler_logger.GENERIC_PYTHON_LOGGER_LOG(self.crawler_logger.LOGGER_LOG_LEVEL_ERROR, "crawler_update_url_index_db: Remove Failed for " + crawler_update_input_url + " from " + str(crawler_list_name) + " with exception ValueError")
            except IndexError:
                self.crawler_logger.GENERIC_PYTHON_LOGGER_LOG(self.crawler_logger.LOGGER_LOG_LEVEL_ERROR, "crawler_update_url_index_db: Remove Failed for " + crawler_update_input_url + " from " + str(crawler_list_name) + " with exception IndexError")
            else:
                self.crawler_logger.GENERIC_PYTHON_LOGGER_LOG(self.crawler_logger.LOGGER_LOG_LEVEL_ERROR, "crawler_update_url_index_db: Remove Success for " + crawler_update_input_url + " from " + str(crawler_list_name))
                
                
    # Function to parse html resources received from page
    def crawler_parse_html_res(self, crawler_html_res):
        crawler_local_tmp_page = 0
        crawler_local_tmp_ref_idx_list = []
        crawler_local_retrieved_url = ""
        
        while(crawler_local_tmp_page != self.CRAWLER_ERROR):
            crawler_local_tmp_page = crawler_html_res.find('<a href', crawler_local_tmp_page + 1)
            crawler_local_tmp_ref_idx_list.append(crawler_local_tmp_page)
            
        for crawler_html_res_start_tag in crawler_local_tmp_ref_idx_list:
            if(crawler_html_res_start_tag == self.CRAWLER_ERROR):
                break
            
            crawler_local_tmp_page = crawler_html_res.find('>', crawler_html_res_start_tag)
            
            if(crawler_local_tmp_page == self.CRAWLER_ERROR):
                self.crawler_logger.GENERIC_PYTHON_LOGGER_LOG(self.crawler_logger.LOGGER_LOG_LEVEL_ERROR, "crawler_parse_html_res: Critical Error - HTML Reference end tag not found")
                return self.CRAWLER_ERROR
            
            self.crawler_logger.GENERIC_PYTHON_LOGGER_LOG(self.crawler_logger.LOGGER_LOG_LEVEL_DEBUG, "crawler_parse_html_res: Fetching url from sliced string " + crawler_html_res[crawler_html_res_start_tag:(crawler_local_tmp_page + 1)])
            crawler_local_retrieved_url = self.crawler_fetch_url_from_str(crawler_html_res[crawler_html_res_start_tag:(crawler_local_tmp_page + 1)])
            
            if(crawler_local_retrieved_url != "CRAWLER_ERROR"):
                # Check if crawled already
                if(self.crawler_check_in_crawled_url_index_db(crawler_local_retrieved_url) == self.CRAWLER_FOUND):
                    self.crawler_logger.GENERIC_PYTHON_LOGGER_LOG(self.crawler_logger.LOGGER_LOG_LEVEL_DEBUG, "crawler_parse_html_res: Page already crawled")
                else:                 
                    self.crawler_update_url_index_db(self.crawler_to_crawl, 'add', crawler_local_retrieved_url)
            else:
                self.crawler_logger.GENERIC_PYTHON_LOGGER_LOG(self.crawler_logger.LOGGER_LOG_LEVEL_ERROR, "crawler_parse_html_res: Critical Error - url retrievel failed")
    
    
    # Function to retrieve url from reference tag       
    def crawler_fetch_url_from_str(self, crawler_input_html_res_ref):

    # Remove spaces from left and right sides    
        crawler_input_html_res_ref.lstrip()
        crawler_input_html_res_ref.rstrip()
        
    # Remove starting characters and spaces before link
        crawler_local_fetch_temp_start = crawler_input_html_res_ref.find('=')
        crawler_local_fetch_temp_end = crawler_input_html_res_ref.find('>', crawler_local_fetch_temp_start)
        
        crawler_local_fetched_string = crawler_input_html_res_ref[(crawler_local_fetch_temp_start + 1) : crawler_local_fetch_temp_end]
        crawler_local_fetched_string.lstrip()
        crawler_local_fetched_string.rstrip()
        
        if(crawler_local_fetched_string[0] == '"'):
            crawler_local_fetched_string = crawler_local_fetched_string[1:(crawler_local_fetched_string.find('"', 2))]
        self.crawler_logger.GENERIC_PYTHON_LOGGER_LOG(self.crawler_logger.LOGGER_LOG_LEVEL_DEBUG, "crawler_fetch_url_from_str: Fetched url - " + crawler_local_fetched_string)
        return crawler_local_fetched_string
    
    
    # Function to check, if url is already crawled
    def crawler_check_in_crawled_url_index_db(self, crawler_retrieved_url_in):
        for crawler_local_crawled_url_index_ctr in self.crawler_crawled:
            if(crawler_local_crawled_url_index_ctr == crawler_retrieved_url_in):
                return self.CRAWLER_FOUND
            
        return self.CRAWLER_NOT_FOUND
    
    
    # Function that starts crawling
    def crawler_crawl(self):
        while(len(self.crawler_to_crawl) > 0):
            crawler_local_temp = self.crawler_get_html_res(self.crawler_to_crawl[0])
            self.crawler_parse_html_res(str(crawler_local_temp))