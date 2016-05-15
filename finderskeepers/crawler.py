# ##########################################################################################
#                                        IMPORTS
# ##########################################################################################

import urllib.request


# ##########################################################################################
#                                        GLOBALS
# ##########################################################################################

# The seed url to start crawling from
crawler_seed = 'https://www.udacity.com/cs101x/index.html'

# Some Typical Macros in form of global variables
CRAWLER_ERROR = -1
CRAWLER_SUCCESS = 1

CRAWLER_FOUND = CRAWLER_SUCCESS
CRAWLER_NOT_FOUND = CRAWLER_ERROR

CRAWLER_TRUE = CRAWLER_SUCCESS
CRAWLER_FALSE = CRAWLER_ERROR

# The two lists, to track the pages to be crawled and already crawled
crawler_to_crawl = [crawler_seed]
crawler_crawled = []


# ##########################################################################################
#                                        FUNCTIONS
# ##########################################################################################


# #############################################
# Function to get HTML Resources from url
# #############################################
def crawler_get_html_res(crawler_input_page):

    print("crawler_get_html_res: Getting links from url " + crawler_input_page)
    with urllib.request.urlopen(crawler_input_page, None, 3) as response:
        crawler_local_read_html = response.read()
        crawler_update_url_index_db(crawler_to_crawl, 'delete', crawler_input_page)
        crawler_update_url_index_db(crawler_crawled, 'add', crawler_input_page)
        return (crawler_local_read_html)


# #############################################
# Function to update the crawler lists with 
# appropriate function, at provided index (url)
# #############################################
def crawler_update_url_index_db(crawler_list_name, crawler_list_function, crawler_update_input_url):
    if(crawler_list_function == 'add'):
        crawler_list_name.append(crawler_update_input_url)
        if(crawler_list_name == crawler_crawled):
            print("crawler_update_url_index_db: Add Success for " + crawler_update_input_url + " to crawler_crawled")
        else:
            print("crawler_update_url_index_db: Add Success for " + crawler_update_input_url + " to crawler_to_crawl")
            
    if(crawler_list_function == 'delete'):
        try:
            crawler_list_name.remove(crawler_update_input_url)
        except ValueError:
            print("crawler_update_url_index_db: Remove Failed for " + crawler_update_input_url + " from " + str(crawler_list_name) + " with exception ValueError")
        except IndexError:
            print("crawler_update_url_index_db: Remove Failed for " + crawler_update_input_url + " from " + str(crawler_list_name) + " with exception IndexError")
        else:
            print("crawler_update_url_index_db: Remove Success for " + crawler_update_input_url + " from " + str(crawler_list_name))
            
            
# #############################################
# Function to parse html resources received 
# from page
# #############################################
def crawler_parse_html_res(crawler_html_res):
    crawler_local_tmp_page = 0
    crawler_local_tmp_ref_idx_list = []
    crawler_local_retrieved_url = ""
    
    while(crawler_local_tmp_page != CRAWLER_ERROR):
        crawler_local_tmp_page = crawler_html_res.find('<a href', crawler_local_tmp_page + 1)
        crawler_local_tmp_ref_idx_list.append(crawler_local_tmp_page)
        
    for crawler_html_res_start_tag in crawler_local_tmp_ref_idx_list:
        if(crawler_html_res_start_tag == CRAWLER_ERROR):
            break
        
        crawler_local_tmp_page = crawler_html_res.find('>', crawler_html_res_start_tag)
        
        if(crawler_local_tmp_page == CRAWLER_ERROR):
            print("crawler_parse_html_res: Critical Error - HTML Reference end tag not found")
            return CRAWLER_ERROR
        
#        print("crawler_parse_html_res: Fetching url from sliced string " + crawler_html_res[crawler_html_res_start_tag:(crawler_local_tmp_page + 1)])
        crawler_local_retrieved_url = crawler_fetch_url_from_str(crawler_html_res[crawler_html_res_start_tag:(crawler_local_tmp_page + 1)])
        
        if(crawler_local_retrieved_url != "CRAWLER_ERROR"):
            # Check if crawled already
            if(crawler_check_in_crawled_url_index_db(crawler_local_retrieved_url) == CRAWLER_FOUND):
                print("crawler_parse_html_res: Page already crawled")
            else:                 
                crawler_update_url_index_db(crawler_to_crawl, 'add', crawler_local_retrieved_url)
        else:
            print("crawler_parse_html_res: Critical Error - url retrievel failed")


# #############################################
# Function to retrieve url from reference tag  
# #############################################          
def crawler_fetch_url_from_str(crawler_input_html_res_ref):
    crawler_local_fetch_temp_start = 0
    crawler_local_fetch_temp_end = 0
    crawler_local_fetched_string = ""
    
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
#    print("crawler_fetch_url_from_str: Fetched url - " + crawler_local_fetched_string)
    return crawler_local_fetched_string


# #############################################
# Function to check, if url is already crawled
# #############################################
def crawler_check_in_crawled_url_index_db(crawler_retrieved_url_in):
    for crawler_local_crawled_url_index_ctr in crawler_crawled:
        if(crawler_local_crawled_url_index_ctr == crawler_retrieved_url_in):
            return CRAWLER_FOUND
        
    return CRAWLER_NOT_FOUND


# ##########################################################################################
#                                        SOURCE ENTRY POINT
# ##########################################################################################

while(len(crawler_to_crawl) > 0):
    crawler_global_local_temp = crawler_get_html_res(crawler_to_crawl[0])
    crawler_parse_html_res(str(crawler_global_local_temp))
    print("")