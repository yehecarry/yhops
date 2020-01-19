#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Author : Yehe
date   : 2020/1/19 11:58
role   : 常量管理与字典管理
"""

from enum import IntEnum as Enum


class ConstError(TypeError):
    pass


class IntEnum(Enum):
    @staticmethod
    def find_enum(cls, value):
        for k, v in cls._value2member_map_.items():
            if k == value:
                return v
        return None


class ErrorCode(IntEnum):
    """ 错误码枚举 """

    not_found = 404
    bad_request = 400
    unauthorized = 401
    forbidden = 403
    not_allowed = 405
    not_acceptable = 406
    conflict = 409
    gone = 410
    precondition_failed = 412
    request_entity_too_large = 413
    unsupport_media_type = 415
    internal_server_error = 500
    service_unavailable = 503
    service_not_implemented = 501
    handler_uncatched_exception = 504
    config_import_error = 1001
    config_item_notfound_error = 1002


class _const(object):
    """
    定义一个字典的方法
    """
    def __setattr__(self, name, value):
        # if name in self.__dict__:
        #     raise ConstError("Can't rebind const (%s)" % name)
        if not name.isupper():
            raise ConstError("Const must be upper.")
        self.__dict__[name] = value


const = _const()

# AWS 配置
const.AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
const.AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
const.REGION_NAME = "REGION_NAME"
const.BUCKET_NAME = "BUCKET_NAME"
const.LOCAL_PATH = "LOCAL_PATH"
const.BACKUP_PATH = "BACKUP_PATH"

# MYSQL 连接配置
const.MYSQL_USER = "MYSQL_USER"
const.MYSQL_PASS = "MYSQL_PASS"
const.MYSQL_IP = "MYSQL_IP"
const.MYSQL_PORT = "MYSQL_PORT"
const.MYSQL_DATABASE = "MYSQL_DATABASE"

# Mondogb 连接配置
const.MONGODB_USER = "MONGODB_USER"
const.MONGODB_PASS = "MONGODB_PASS"
const.MONGODB_IP = "MONGODB_IP"
const.MONGODB_PORT = "MONGODB_PORT"
const.MONGODB_DATABASE = "MONGODB_DATABASE"
const.MONGODB_REPLSET = "MONGODB_REPLSET"

# Redis 连接配置
const.REDIS_PASS = "REDIS_PASS"
const.REDIS_IP = "REDIS_IP"
const.REDIS_PORT = "REDIS_PORT"
const.REDIS_DATABASE = "REDIS_DATABASE"
const.REDIS_MASTER_NAME = "REDIS_MASTER_NAME"
const.REDIS_RDB_PATH = "REDIS_RDB_PATH"


