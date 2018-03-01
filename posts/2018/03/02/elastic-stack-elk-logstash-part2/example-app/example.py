#!/usr/bin/env python

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s '
                           '%(process)d %(thread)d '
                           '%(name)s %(funcName)s %(lineno)s '
                           '%(message)s',
                    level=logging.DEBUG,
                    filename="/var/log/example-app/example.log")
logger = logging.getLogger('example')


def do_something():
    logger.debug('I did something!')


def main():
    logger.info('Started the application.')
    do_something()


if __name__ == '__main__':
    main()
