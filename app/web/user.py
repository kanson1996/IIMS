#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2019/12/30 15:09.
"""

from datetime import datetime

from flask import jsonify, request
from flask_login import login_user

from app.models.base import db
from app.models.user import User
from app.utils.datetime_util import utc2local, time_judge
from . import web


error_of_phone = {}


@web.route ('/register', methods=['GET', 'POST'])
def register():
    phone_number = request.args['phone_number']
    user = User.query.filter_by (phone_number=phone_number).first ()
    if user:
        print ('当前手机号已存在（被注册）')
        return jsonify ({'code': 1, 'msg': '当前手机号已存在（被注册）'})
    else:
        user = User ()
        user.set_attrs (request.args)
        db.session.add (user)
        db.session.commit ()
        return jsonify ({'code': 0})


# 约定：1、手机号不存在，提示未注册，2、如果密码错误，提示密码错误
#      3、服务端缓存连续输错的次数 >=3 以后限制，做定时功能，过期之后缓存输错数目归零，可重新登录
#       并且当输入错误的时候，要向用户返回连续几次登录失败，请注意！
#       4、修改密码
@web.route ('/login', methods=['GET', 'POST'])
def login():
    phone_number = request.args['phone_number']
    password = request.args['password']
    code = request.args['code']

    user = User.query.filter_by (phone_number=phone_number).first ()
    # 每次登录，到达服务端时候，先对error_of_phone中输入错误次数达到3次的手机号进行更新。即判定当前时间到上次时间超过30分钟的手机号，将其从error_of_phone中删除
    if user is None:
        print ('当前输入用户无效')
        return jsonify ({'code': 1, 'msg': '当前输入用户无效'})
    now_time = utc2local (datetime.utcnow ())
    # 锁住，判断时间间隔
    if user.locked is True:
        last_time = datetime.strptime (str (user.last_time), "%Y-%m-%d %H:%M:%S")  # 字符串转时间
        str_now_time = now_time.strftime ("%Y-%m-%d %H:%M:%S")
        now_time = datetime.strptime (str_now_time, "%Y-%m-%d %H:%M:%S")  # datetime
        print (last_time, type (last_time))
        print (now_time, type (now_time))
        if time_judge (last_time, now_time) >= 30:
            user.locked = False  # 更新锁状态
            db.session.add (user)
            db.session.commit ()
        else:
            print ('仍处于30分钟限制中，请稍后操作')
            return jsonify ({'code': 1, 'phone_number': phone_number, 'passowrd': password, 'msg': '手机号不存在或密码错误',
                             'phone': {'errNums': error_of_phone[phone_number]}})
    # 没有锁住，就正常登录
    if user.locked is False:
        if user and user.check_password (password):
            login_user (user, remember=True)
            user.last_time = now_time.strftime ("%Y-%m-%d %H:%M:%S")  # 更新登录时间
            db.session.add (user)
            db.session.commit ()
            return jsonify ({'code': 0, 'phone_number': phone_number, 'passowrd': password, 'msg': '登录成功',
                             'result': {'nickname': user.nickname, 'phone_number': user.phone_number}})
        else:
            print ('账号不存在或密码错误')
            if phone_number not in error_of_phone.keys ():
                error_of_phone[phone_number] = 1
                print ('if ' + str (error_of_phone[phone_number]))
            else:
                error_of_phone[phone_number] = error_of_phone[phone_number] + 1
                print ('else ' + str (error_of_phone[phone_number]))
                if (error_of_phone[phone_number] == 3):
                    user.locked = True  # 锁住
                    user.last_time = now_time.strftime ("%Y-%m-%d %H:%M:%S")  # 更新登录时间
                    db.session.add (user)
                    db.session.commit ()
        print ('after ' + str (error_of_phone[phone_number]))
        return jsonify ({'code': 1, 'phone_number': phone_number, 'passowrd': password, 'msg': '手机号不存在或密码错误',
                         'phone': {'errNums': error_of_phone[phone_number]}})


@web.route ('/validatorPwd', methods=['GET', 'POST'])
def validatorPwd():
    phone_number = request.args['phone_number']
    old_password = request.args['old_password']
    new_password = request.args['new_password']
    user = User.query.filter_by (phone_number=phone_number).first ()
    if user and user.check_password (old_password):
        print ('校验通过')
        user.password = new_password
        db.session.add (user)
        db.session.commit ()
        return jsonify ({'validator': 1})
    else:
        print ('校验不通过')
        return jsonify ({'validator': 0})


@web.route ('/changePwd', methods=['GET', 'POST'])
def changePwd():
    user = User ()
    user.set_attrs (request.args)
    db.session.add (user)
    db.session.commit ()
    print ('修改成功')
    return jsonify ({'code': 0})
