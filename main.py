#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2019/12/31 22:30.
"""
from app import create_app

app = create_app ()

# 入口文件
if __name__ == '__main__':
    # 生产环境 nginx+uwsgi
    # 加入判断语句，就不会执行flask的配置语句，而是使用生产环境配置
    app.run (host='0.0.0.0', debug=app.config['DEBUG'], threaded=True)
    # 单进程，单线程
    # threaded = True process = True
