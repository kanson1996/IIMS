#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/12 16:03.
"""
import random

import datetime


def tid_maker():
    a = int (datetime.datetime.now ().timestamp ())
    b = int (''.join ([str (random.randint (0, 9)) for i in range (3)]))
    a = str (a)
    b = str (b)
    c = a + b
    return c
