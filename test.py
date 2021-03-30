#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import time
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
        fast_log.add_log('test log write performance')
    while fast_log.is_writing:
        time.sleep(0.01)


if __name__ == "__main__":
    test_fast_log = FastLog()
    # test_performance calc time: 2.0698201656341553
    test_performance(test_fast_log)
