#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# description   : Logging module with rich
# ----------------------------------------------------------------------------

import logging
from rich.logging import RichHandler
logging.basicConfig(level='NOTSET', format='%(message)s', datefmt='[%X]', handlers=[RichHandler()])

log = logging.getLogger()
log.debug('Start of program')


def factorial(n):
    log.debug('Start of factorial(%s)' % (n))
    total = 1
    for i in range(1, n + 1):
        total *= i
        log.debug('i is {}, total is {}'.format(i, total))
    log.debug('End of facotrial(%s)' % (n))
    return total


# nice example
num = input('[?] Enter a number: ')
print('Factorial of {} is {}'.format(num, factorial(5)))
log.debug('End of program')
log.error('[bold red blink]Server is shutting down![/]', extra={'markup': True})
