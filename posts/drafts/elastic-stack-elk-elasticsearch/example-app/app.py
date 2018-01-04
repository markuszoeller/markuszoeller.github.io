#!/usr/bin/env python

from flask import Flask
import json
import logging.handlers
import requests


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
        }
        r = requests.post(self.url,
                          data=json.dumps(payload),
                          headers=headers)
        print("Log record emit result: %s" % r.status_code)


http_handler = ElasticsearchHandler("http://es1:9200/app/logs/")
http_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s - %(asctime)s')
http_handler.setFormatter(http_formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(http_handler)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
