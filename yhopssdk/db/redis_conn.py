#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Author : Yehe
date   : 2020/1/19 15:06
role   : Redis 通用方法
"""

import os
import sys
import redis
from redis.sentinel import Sentinel
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
from yhopssdk.pubilc.const import const


class RedisConn(object):
    def __init__(self, data):
        self.redis_pass = const.REDIS_PASS
        self.redis_ip = data.REDIS_IP
        self.redis_port = data.REDIS_PORT
        self.redis_database = const.REDIS_DATABASE
        self.redis_master_name = data.REDIS_MASTER_NAME

    def redis_sentinel_conn(self):
        # 生成ip列表
        cluster_ip = []
        for i in range(len(self.redis_ip)):
            cluster_ip.append((self.redis_ip[i], self.redis_port[i]))
        sentinel = Sentinel(cluster_ip, socket_timeout=0.5)
        return sentinel

    def get_master_ip(self):
        sentinel = self.redis_sentinel_conn()
        master = sentinel.discover_master(self.redis_master_name)
        return master

    def get_slave_ip(self):
        sentinel = self.redis_sentinel_conn()
        slave = sentinel.discover_slaves(self.redis_master_name)
        return slave

    def backup_redis(self):
        sentinel = self.redis_sentinel_conn()
        slave = sentinel.slave_for(self.redis_master_name, socket_timeout=0.5, password=self.redis_pass, db=self.redis_database)
        ret = slave.bgsave()
        return ret




        # slave_ip = self.get_slave_ip()
        # for
        # print(slave_ip)


if __name__ == '__main__':
    const.REDIS_IP = ["192.168.1.84", "192.168.1.84", "192.168.1.84"]
    const.REDIS_PORT = ["26379", "26380", "26381"]
    const.REDIS_MASTER_NAME = "mymaster"
    client = RedisConn(const)
    client.backup_redis()
