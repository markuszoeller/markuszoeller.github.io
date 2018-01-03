#!/usr/bin/env python

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

        print(r.status_code)


http_handler = ElasticsearchHandler("http://192.168.78.11:9200/app/logs/")
http_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s - %(asctime)s')
http_handler.setFormatter(http_formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(http_handler)

logger.info('info message')
logger.debug('debug message')
logger.warning('warning message')

