#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import os
import time
import logging
from fast_log import FastLog


def calc_time(func):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        result = func(*args,**kwargs)
        end_time = time.time()
        print("{} calc time: {}".format(func.__name__,end_time-start_time))
        return result
    return wrapper


@calc_time
def test_performance(fast_log):
    for i in range(100000):
        fast_log.add_log(fast_log.INFO, 'test log write performance')
    while fast_log.is_writing:
        time.sleep(0.01)


@calc_time
def test_logging__performance():
    for i in range(100000):
        logging.log(logging.INFO, 'test log write performance')


if __name__ == "__main__":
    test_fast_log = FastLog()

    # test_performance calc time: 2.0698201656341553
    test_performance(test_fast_log)
    # test clear
    test_fast_log.clear_old_log(3, 100)

    # test_logging__performance calc time: 6.841032981872559
    test_logging_path = 'logs//test_logging.log'
    if os.path.exists(test_logging_path):
        os.remove(test_logging_path)
    logging.basicConfig(filename=test_logging_path,
                        format='[%(asctime)s-%(levelname)s:%(message)s]', level=logging.INFO,
                        filemode='a+', datefmt='%Y-%m-%d%I:%M:%S %p')
    test_logging__performance()