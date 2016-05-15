# Log Levels
LOGGER_LOG_LEVEL_NONE      = 0    # - 0000
LOGGER_LOG_LEVEL_TRACE     = 1    # - 0001
LOGGER_LOG_LEVEL_ERROR     = 2    # - 0010
LOGGER_LOG_LEVEL_DEBUG     = 4    # - 0100
LOGGER_LOG_LEVEL_ALL       = 7    # - 0111

LOGGER_LOG_LEVEL = -1


def GENERIC_PYTHON_LOGGER_INIT (logger_log_level_in):
    LOGGER_LOG_LEVEL = logger_log_level_in

def GENERIC_PYTHON_LOGGER (logger_log_str_in, logger_log_level_in):
    if(LOGGER_LOG_LEVEL & logger_log_level_in)