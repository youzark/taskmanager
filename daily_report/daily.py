#!/usr/bin/env python
import time

def get_date():
    time_stamp = time.time()
    date = time.localtime(time_stamp)
    fmt_date = f"{date.tm_year}_{date.tm_mon}_{date.tm_mday}"
    return fmt_date

class daily:
    def __init__(self):
        time = get_date()
        self.path = "/home/hyx/data/taskmanager_daily/" +time + ".json"
        with open(self.path,'w') as f:
            pass




