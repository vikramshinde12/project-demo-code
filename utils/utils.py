from datetime import datetime
import re
import uuid
import yaml

#from common.const import DATAFLOW, BIG_QUERY
from zipfile import ZipFile
from utils.logging import get_logging_client

logging = get_logging_client()




def get_file_from_zip(filename):
    zipfile, post_zip = re.search(r'(.*\.zip)?(.*)', filename).groups()
    logging.info("zip={} and post_zip={}".format(zipfile, post_zip))
    if zipfile:
        return ZipFile(zipfile).read(post_zip.lstrip('/'))
    else:
        return open(post_zip).read()

