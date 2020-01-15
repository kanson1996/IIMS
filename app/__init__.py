#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2019/12/30 15:09.
"""

from flask import Flask
from flask_login import LoginManager

from app.models.base import db

login_manager = LoginManager ()


def register_blueprint(app):
    from app.web import web
    app.register_blueprint (web)


def create_app():
    app = Flask (__name__)  # 操作Flask核心对象
    app.config.from_object ('app.secure')
    db.init_app (app)
    login_manager.init_app (app)
    register_blueprint (app)
    db.create_all (app=app)
    return app
