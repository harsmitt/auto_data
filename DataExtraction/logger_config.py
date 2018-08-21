import logging
import os
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

path = os.path.join('/home/mahima/logs/')
if not os.path.exists(path):
    try:
        os.makedirs(path)
    except Exception as e:
        import traceback
        print (traceback.format_exc())
import time
timestr = time.strftime("%Y-%m-%d")

file_name = path+'dataautomation_log_%s.log' %(timestr)
# create a file handler

handler = logging.FileHandler(file_name)
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s -(fname)-12s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

path = '/home/mahima/logs/'

