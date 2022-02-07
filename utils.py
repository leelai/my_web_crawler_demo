import random
import time

import os
import os.path
import time
import logging
import datetime as dt

timeout = 5 # http request timeout(seconds)
min = 0.5 # delay min seconds
max = 1.0 # delay max seconds

def delay():
    time.sleep(random.uniform(min, max))

LOG_FILE = os.path.join(os.getcwd() , 'logs')
logFormatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")

# LOG_FILE_2 = os.path.join(LOG_FILE , dt.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S') + "error.log")
# file_handler = logging.FileHandler("{0}".format(LOG_FILE_2))
# file_handler.setFormatter(logFormatter)
# file_handler.setLevel(logging.ERROR)
# logger = logging.getLogger('http_err')
# logger.addHandler(file_handler)

def initLog():
    if not os.path.exists(LOG_FILE):
        os.makedirs(LOG_FILE)
    LOG_FILE_1 = os.path.join(LOG_FILE , dt.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S') + ".log")
    # LOG_FILE = LOG_FILE + "/" + dt.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S') + ".log"
    fileHandler = logging.FileHandler("{0}".format(LOG_FILE_1))
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.INFO)
    rootLogger = logging.getLogger()
    rootLogger.addHandler(fileHandler)
    rootLogger.setLevel(logging.INFO)

