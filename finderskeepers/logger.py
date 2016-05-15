# ##########################################################################################
#                                        GLOBALS
# ##########################################################################################
# Log Levels

class generic_python_logger:
    LOGGER_LOG_LEVEL_NONE      = 0    # - 0000
    LOGGER_LOG_LEVEL_TRACE     = 1    # - 0001
    LOGGER_LOG_LEVEL_ERROR     = 2    # - 0010
    LOGGER_LOG_LEVEL_DEBUG     = 4    # - 0100
    LOGGER_LOG_LEVEL_ALL       = 7    # - 0111

    LOGGER_LOG_LEVEL_TRACE_STR = "LOGGER_LOG_LEVEL_TRACE"
    LOGGER_LOG_LEVEL_ERROR_STR = "LOGGER_LOG_LEVEL_ERROR"
    LOGGER_LOG_LEVEL_DEBUG_STR = "LOGGER_LOG_LEVEL_DEBUG"

    LOGGER_LOG_LEVEL = 0

    # #############################################
    # Function to Initialise logger
    # #############################################
    def __init__(self, logger_log_level_in):
        self.LOGGER_LOG_LEVEL = logger_log_level_in
        return;


    # #############################################
    # Function called by external entities
    # It checks log level string, and readies the
    # end string to be printed on console
    # #############################################
    def GENERIC_PYTHON_LOGGER_LOG (self, logger_log_level_str_in, logger_log_str_in):
        if(logger_log_level_str_in == self.LOGGER_LOG_LEVEL_TRACE_STR):
            logger_log_str_in = self.LOGGER_LOG_LEVEL_TRACE_STR + logger_log_str_in
            self.GENERIC_LOGGER_PRINT_LOG (logger_log_str_in, self.LOGGER_LOG_LEVEL_TRACE)
            return;
    
        if(logger_log_level_str_in == self.LOGGER_LOG_LEVEL_ERROR_STR):
            logger_log_str_in = self.LOGGER_LOG_LEVEL_ERROR_STR + logger_log_str_in
            self.GENERIC_LOGGER_PRINT_LOG (logger_log_str_in, self.LOGGER_LOG_LEVEL_ERROR)
            return;
            
        if(logger_log_level_str_in == self.LOGGER_LOG_LEVEL_DEBUG_STR):
            logger_log_str_in = self.LOGGER_LOG_LEVEL_DEBUG_STR + logger_log_str_in
            self.GENERIC_LOGGER_PRINT_LOG (logger_log_str_in, self.LOGGER_LOG_LEVEL_DEBUG)
            return;
    
        
    # #############################################
    # Function to check log level, and print string
    # #############################################
    def GENERIC_LOGGER_PRINT_LOG (self, logger_log_str_in, logger_log_level_in):
        if( ((self.LOGGER_LOG_LEVEL & logger_log_level_in) == logger_log_level_in) or 
            ((self.LOGGER_LOG_LEVEL & logger_log_level_in) == self.LOGGER_LOG_LEVEL_ALL) ):
            print(logger_log_str_in)
            return