#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/12 19:13.
"""

import time
import datetime


# 判断间隔时间
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


# 生成当前时间的时间戳，只有一个参数即时间戳的位数，默认为10位，输入位数即生成相应位数的时间戳，比如可以生成常用的13位时间戳
def now_to_timestamp(digits=10):
    time_stamp = time.time ()
    digits = 10 ** (digits - 10)
    time_stamp = int (round (time_stamp * digits))
    return time_stamp


# 将时间戳规范为10位时间戳
def timestamp_to_timestamp10(time_stamp):
    time_stamp = int (time_stamp * (10 ** (10 - len (str (time_stamp)))))
    return time_stamp


# 将当前时间转换为时间字符串，默认为2017-10-01 13:37:04格式
def now_to_date(format_string="%Y-%m-%d %H:%M:%S"):
    time_stamp = int (time.time ())
    time_array = time.localtime (time_stamp)
    str_date = time.strftime (format_string, time_array)
    return str_date


# 将10位时间戳转换为时间字符串，默认为2017-10-01 13:37:04格式
def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.localtime (time_stamp)
    str_date = time.strftime (format_string, time_array)
    return str_date


# 将时间字符串转换为10位时间戳，时间字符串默认为2017-10-01 13:37:04格式
def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime (date, format_string)
    time_stamp = int (time.mktime (time_array))
    return time_stamp


# 不同时间格式字符串的转换
def date_style_transfomation(date, format_string1="%Y-%m-%d %H:%M:%S", format_string2="%Y-%m-%d %H-%M-%S"):
    time_array = time.strptime (date, format_string1)
    str_date = time.strftime (format_string2, time_array)
    return str_date


def str2date(str, date_format="%Y-%m-%d"):
    date = datetime.datetime.strptime (str, date_format)
    return date


def date2str(date, date_formate="%Y%m%d"):
    str = date.strftime (date_formate)
    return str


def date_delta(date, gap, formate="%Y%m%d"):
    date = str2date (date)
    pre_date = date + datetime.timedelta (days=-gap)
    pre_str = date2str (pre_date, formate)  # date形式转化为str
    return pre_str


def str2timestamp(str, timestamp_len=10):
    date_array = time.strptime (str, "%Y-%m-%d %H:%M:%S")
    timestamp = int (time.mktime (date_array))
    if timestamp_len == 13:
        timestamp *= 1000
    return timestamp
