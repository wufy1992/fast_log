#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import os
import time
import threading
import queue


class FastLog(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.max_log_queue = 100000
        self.write_batch_size = 100
        self.max_file_size = 4 * 1024 * 1024
        self.enable_log = True
        self.log_queue = queue.Queue(self.max_log_queue)
        self.is_writing = False
        self.logs_dir = 'logs'
        if not os.path.exists(self.logs_dir):
            os.mkdir(self.logs_dir)
        self.log_file_path = self.get_new_log_file_path()

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            with FastLog._instance_lock:
                if not hasattr(cls, '_instance'):
                    FastLog._instance = super().__new__(cls)
            return FastLog._instance

    def get_new_log_file_path(self):
        return os.path.join(self.logs_dir, time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + '.log')

    def stop_log(self):
        self.enable_log = False

    def start_log(self):
        self.enable_log = True

    def add_log(self, log_str):
        if not self.enable_log:
            return
        log_info = dict()
        log_info['log'] = log_str
        log_info['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if self.log_queue.qsize() > self.max_log_queue / 100 and not self.is_writing:
            write_log_thread = threading.Thread(target=self.write_log)
            write_log_thread.start()
        try:
            self.log_queue.put(log_info, block=True, timeout=0.001)
        except queue.Full:
            while self.log_queue.full():
                time.sleep(0.001)
            self.log_queue.put(log_info, block=True, timeout=0.001)

    def write_log(self):
        self.is_writing = True
        log_list = list()
        log_file = open(self.log_file_path, 'a+')
        while not self.log_queue.empty():
            log_info = self.log_queue.get(block=True, timeout=10)
            log_list.append("{time}:\t{log}\n".format(time=log_info['time'], log=log_info['log']))
            if len(log_list) > self.write_batch_size:
                if os.path.exists(self.log_file_path) and os.path.getsize(self.log_file_path) > self.max_file_size:
                    self.log_file_path = self.get_new_log_file_path()
                    log_file = open(self.log_file_path, 'a+')
                log_file.write(''.join(log_list))
                log_list = list()
        self.is_writing = False

