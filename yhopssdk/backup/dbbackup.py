#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Author : Yehe
date   : 2020/1/17 10:14
role   : 备份数据库
"""

import sys
import os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
from yhopssdk.pubilc.operate import exec_shell


class DbBackup(object):
    """
    备份脚本
    支持mysql mongodb redis 数据库备份
    """

    def __init__(self, service, data):
        # 定义 路径
        self.service = service
        _hostname = exec_shell("hostname")[1]
        _data = exec_shell("date +%Y%m%d")[1]
        self.local_path = "/backup/{hostname}/{service}/{data}".\
            format(hostname=_hostname, service=self.service, data=_data)
        # 定义mysql
        self.mysql_user = data.MYSQL_USER
        self.mysql_pass = data.MYSQL_PASS
        self.mysql_ip = data.MYSQL_IP
        self.mysql_port = data.MYSQL_PORT
        self.mysql_database = data.MYSQL_DATABASE
        # 定义mongodb
        self.mongodb_user = data.MONGODB_USER
        self.mongodb_pass = data.MONGODB_PASS
        self.mongodb_ip = data.MONGODB_IP
        self.mongodb_port = data.MONGODB_PORT
        self.mongodb_database = data.MONGODB_DATABASE
        self.mongodb_replset = data.MONGODB_REPLSET

    def mysql_backup(self):
        """
        mysql 备份方法
        :return:
        """
        # 单库全量备份备份
        if not os.path.exists(self.local_path):
            exec_shell("mkdir -p {path}".format(path=self.local_path))
        local_path = self.local_path + "/" + self.mysql_database + ".sql.gz"
        exec_shell("mysqldump -u {user} -p{password} -p {port} -h {ip} --database {database} --skip-lock-table"
                   "|gzip > {local_path}".format(user=self.mysql_user, password=self.mysql_pass, ip=self.mysql_ip,
                                                 port=self.mysql_port, database=self.mysql_database,
                                                 local_path=local_path))
        backup_path = local_path[1:]
        return local_path, backup_path
        # 增量备份

    def mysql_all_backup(self):
        """
        mysql 备份方法
        :return:
        """
        # 全库全量备份备份
        if not os.path.exists(self.local_path):
            exec_shell("mkdir -p {path}".format(path=self.local_path))
        local_path = self.local_path + "/" + self.mysql_database + ".sql.gz"
        exec_shell("mysqldump -u {user} -p{password} -p {port} -h {ip} --database {database} --skip-lock-table"
                   "|gzip > {local_path}".format(user=self.mysql_user, password=self.mysql_pass, ip=self.mysql_ip,
                                                 port=self.mysql_port, database=self.mysql_database,
                                                 local_path=local_path))
        backup_path = local_path[1:]
        return local_path, backup_path
        # 增量备份

    def mongodb_backup(self):
        """
        mongodb 单库备份方法
        :return:
        """
        # 本地备份目录
        local_backup_path = self.local_path + self.mongodb_database
        # 备份文件路径
        local_backup_file_path = self.local_path + "/" + self.mongodb_database + ".gz"
        # 创建备份目录
        if not os.path.exists(local_backup_path):
            exec_shell("mkdir -p {path}".format(path=local_backup_path))
        # 单点单库备份
        if not self.mongodb_replset:
            # 没有用户名与密码
            if not self.mongodb_user:
                exec_shell("mongodump -h {ip}:{port} -d {database} -o {local_path}"
                           .format(ip=self.mongodb_ip, port=self.mongodb_port, database=self.mongodb_database,
                                   local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path
            # 有用户名和密码
            elif self.mongodb_user and self.mongodb_pass:
                exec_shell("mongodump -u {user} -p {password} -h {ip}:{port} -d {database} -o {local_path}"
                           .format(user=self.mongodb_user, password=self.mongodb_pass, ip=self.mongodb_ip,
                                   port=self.mongodb_port, database=self.mongodb_database, local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path
        # 集群单库备份
        else:
            # 生成集群ip 格式
            cluster_ip = []
            for i in range(len(self.mongodb_ip)):
                cluster_ip.append(self.mongodb_ip[i] + ":" + self.mongodb_port[i])
            cluster_ip = ",".join(cluster_ip)
            # 没有用户名与密码
            if not self.mongodb_user:
                exec_shell("mongodump -h {cluster_ip} -d {database} -o {local_path}".format
                           (cluster_ip=cluster_ip, database=self.mongodb_database, local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path
            elif self.mongodb_user and self.mongodb_pass:
                exec_shell("mongodump -u {user} -p {password} -h {cluster_ip} -d {database} -o {local_path}"
                           .format(user=self.mongodb_user, password=self.mongodb_pass, cluster_ip=cluster_ip,
                                   database=self.mongodb_database, local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path

    def mongodb_all_backup(self, mongodb_data):
        """
        mongodb 全库备份方法
        :return:
        """
        # 本地备份目录
        local_backup_path = self.local_path + "/AllDatabase"
        # 备份文件路径
        local_backup_file_path = self.local_path + "/AllDatabase.tar.gz"
        # 创建备份目录
        if not os.path.exists(local_backup_path):
            exec_shell("mkdir -p {path}".format(path=local_backup_path))
        # 单点全库备份
        if not self.mongodb_replset:
            # 没有用户名与密码
            if not self.mongodb_user:
                exec_shell("mongodump -h {ip}:{port} -o {local_path}".format
                           (ip=self.mongodb_ip, port=self.mongodb_port, local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path
            # 有用户名和密码
            elif self.mongodb_user and self.mongodb_pass:
                exec_shell("mongodump -u {user} -p {password} -h {ip}:{port} -o {local_path}"
                           .format(user=self.mongodb_user, password=self.mongodb_pass, ip=self.mongodb_ip,
                                   port=self.mongodb_port, local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path
        # 集群单库备份
        else:
            # 生成集群ip 格式
            cluster_ip = []
            for i in range(len(self.mongodb_ip)):
                cluster_ip.append(self.mongodb_ip[i] + ":" + self.mongodb_ip[i])
            cluster_ip = ",".join(cluster_ip)
            # 没有用户名与密码
            if not self.mongodb_user:
                exec_shell("mongodump -h {cluster_ip}  -o {local_path}".format(cluster_ip=cluster_ip,
                                                                               local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path
            elif self.mongodb_user and self.mongodb_pass:
                exec_shell("mongodump -u {user} -p {password} -h {cluster_ip} -o {local_path}"
                           .format(user=self.mongodb_user, password=self.mongodb_pass, cluster_ip=cluster_ip,
                                   local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path

    def redis_backup(self):
        print("redisrest")

    def redis_all_backup(self):
        print("redisrest")


if __name__ == '__main__':
    print("test")