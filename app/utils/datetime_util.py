#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/16 22:01.
"""


# 判断间隔时间
import time
from datetime import datetime


def time_judge(start_time, end_time):
    total_seconds = (end_time - start_time).total_seconds ()
    # 来获取准确的时间差，并将时间差转换为秒
    mins = total_seconds / 60
    return int (mins)


# UTC时间转本地时间（+8:00）
def utc2local(utc_st):
    now_stamp = time.time ()
    local_time = datetime.fromtimestamp (now_stamp)
    utc_time = datetime.utcfromtimestamp (now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st


# 本地时间转UTC时间（-8:00）
def local2utc(local_st):
    time_struct = time.mktime (local_st.timetuple ())
    utc_st = datetime.utcfromtimestamp (time_struct)
    return utc_st

