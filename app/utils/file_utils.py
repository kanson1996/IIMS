#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/2 17:32.
"""
import os


# 创建create_folder函数，用来判断是否需要生成新的文件夹
def creat_folder(folder_path):
    if not os.path.exists (folder_path):
        os.mkdir (folder_path)
        os.chmod (folder_path, os.O_RDWR)