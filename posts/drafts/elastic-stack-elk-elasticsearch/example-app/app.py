#!/usr/bin/env python

from flask import Flask
import json
import logging.handlers
import platform
import requests

HOSTNAME = platform.node()


# ======================================================================
# Custom logging handler for Elasticsearch
# ======================================================================
class ElasticsearchHandler(logging.Handler):

    def __init__(self, url):
        super(ElasticsearchHandler, self).__init__()
        self.url = url

    def emit(self, record):
        self.format(record)
        headers = {'content-type': 'application/json'}
        payload = {
            'module': record.module,
            'timestamp': record.asctime,
            'level': record.levelname,
            'message': record.message,
            'host': HOSTNAME,
        }
        r = requests.post(self.url,
                          data=json.dumps(payload),
                          headers=headers)
        print("Log record emit result: %s" % r.status_code)


# ======================================================================
# Set up logging
# ======================================================================
formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')

http_handler = ElasticsearchHandler("http://es1:9200/app/logs/")
http_handler.setFormatter(formatter)

file_handler = logging.handlers.RotatingFileHandler("app.log",
                                                    maxBytes=10240,
                                                    backupCount=4)
file_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(http_handler)
logger.addHandler(file_handler)


# ======================================================================
# REST API with Flask
# ======================================================================
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!\n"


@app.route("/logging/debug")
def log_debug_message():
    logger.debug('debug message')
    return "Logged debug message.\n"


@app.route("/logging/info")
def log_info_message():
    logger.info('info message')
    return "Logged info message.\n"


@app.route("/logging/warning")
def log_warning_message():
    logger.warning('warning message')
    return "Logged warning message\n"


# ======================================================================
# MAIN
# ======================================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0')
