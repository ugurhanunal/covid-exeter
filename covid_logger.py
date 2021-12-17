import logging
import json

configData = json.load(open('config.json'))

logging.basicConfig(filename=configData["log_data_filename"],
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def log(row):
    logger.info(row)
