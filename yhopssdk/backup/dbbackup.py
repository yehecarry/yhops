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
from ..pubilc.useshell import exec_shell


class DbBackup(object):
    """
    备份脚本
    支持mysql mongodb redis 数据库备份
    """

    def __init__(self, service):
        # service 从argv[1] 获取
        self.service = service
        _hostname = exec_shell("hostname")[1]
        _data = exec_shell("date +%Y%m%d")[1]
        self.local_path = "/backup/{hostname}/{service}/{data}".format(hostname=_hostname, service=self.service,
                                                                       data=_data)

    def mysql_backup(self, mysql_data):
        """
        mysql 备份方法
        :param user: mysql用户名
        :param password: mysql密码
        :param ip: mysql ip地址
        :param port: mysql 端口号
        :param database:  需要备份的数据库名字
        :return:
        """
        user = mysql_data.get("user")
        password = mysql_data.get("password")
        ip = mysql_data.get("ip")
        port = mysql_data.get("port")
        database = mysql_data.get("database")
        # 单库全量备份备份
        if not os.path.exists(self.local_path):
            exec_shell("mkdir -p {path}".format(path=self.local_path))
        local_path = self.local_path + "/" + database + ".sql.gz"
        exec_shell("mysqldump -u {user} -p{password} -p {port} -h {ip} --database {database}"
                   " --skip-lock-table |gzip > {local_path}".format(user=user, password=password, ip=ip, port=port,
                                                                    database=database, local_path=local_path))
        backup_path = local_path[1:]
        return local_path, backup_path
        # 增量备份

    def mongodb_backup(self, mongodb_data):
        """
        mongodb 单库备份方法
        :param user: mongodb 用户名
        :param password: mongodb 密码
        :param ip: mongodb ip地址
        :param port: mongodb 端口
        :param database: 备份的mongodb数据库名称
        :param replSetName mongodb副本集名称默认是空
        :return:
        """
        # 读取配置信息
        user = mongodb_data.get("user")
        password = mongodb_data.get("password")
        ip = mongodb_data.get("ip")
        port = mongodb_data.get("port")
        database = mongodb_data.get("database")
        rep = mongodb_data.get("rep")

        # 本地备份目录
        local_backup_path = self.local_path + database
        # 备份文件路径
        local_backup_file_path = self.local_path + "/" + database + ".gz"
        # 创建备份目录
        if not os.path.exists(local_backup_path):
            exec_shell("mkdir -p {path}".format(path=self.local_path))
        # 单点单库备份
        if not rep:
            # 没有用户名与密码
            if not user:
                exec_shell("mongodump -h {ip}:{port} -d {database} -o {local_path}".format
                           (ip=ip, port=port, database=database, local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path + database))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path
            # 有用户名和密码
            elif user and password:
                exec_shell("mongodump -u {user} -p {password} -h {ip}:{port} -d {database} -o {local_path}".format
                           (user=user, password=password, ip=ip, port=port, database=database, local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path + database))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path
        # 集群单库备份
        else:
            # 生成集群ip 格式
            cluster_ip = []
            for i in range(len(ip)):
                cluster_ip.append(ip[i] + ":" + port[i])
            cluster_ip = ",".join(cluster_ip)
            # 没有用户名与密码
            if not user:
                exec_shell("mongodump -h {cluster_ip} -d {database} -o {local_path}".format
                           (cluster_ip=cluster_ip, database=database, local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path + database))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path
            elif user and password:
                exec_shell("mongodump -u {user} -p {password} -h {cluster_ip} -d {database} -o {local_path}"
                           .format(user=user, password=password, cluster_ip=cluster_ip, database=database,
                                   local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path + database))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path

    def mongodb_all_backup(self, mongodb_data):
        """
        mongodb 全库备份方法
        :param user: mongodb 用户名
        :param password: mongodb 密码
        :param ip: mongodb ip地址
        :param port: mongodb 端口
        :param database: 备份的mongodb数据库名称
        :param replSetName mongodb副本集名称默认是空
        :return:
        :param mongodb_data:
        :return:
        """
        # 读取配置信息
        user = mongodb_data.get("user")
        password = mongodb_data.get("password")
        ip = mongodb_data.get("ip")
        port = mongodb_data.get("port")
        rep = mongodb_data.get("rep")

        # 本地备份目录
        local_backup_path = self.local_path + "/alldatabase"
        # 备份文件路径
        local_backup_file_path = self.local_path + "/" + "alldatabase.tar.gz"
        # 创建备份目录
        if not os.path.exists(local_backup_path):
            exec_shell("mkdir -p {path}".format(path=local_backup_path))
        # 单点全库备份
        if not rep:
            # 没有用户名与密码
            if not user:
                exec_shell("mongodump -h {ip}:{port} -o {local_path}".format
                           (ip=ip, port=port, local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path
            # 有用户名和密码
            elif user and password:
                exec_shell("mongodump -u {user} -p {password} -h {ip}:{port} -o {local_path}".format
                           (user=user, password=password, ip=ip, port=port, local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path
        # 集群单库备份
        else:
            # 生成集群ip 格式
            cluster_ip = []
            for i in range(len(ip)):
                cluster_ip.append(ip[i] + ":" + port[i])
            cluster_ip = ",".join(cluster_ip)
            # 没有用户名与密码
            if not user:
                exec_shell("mongodump -h {cluster_ip}  -o {local_path}".format(cluster_ip=cluster_ip,
                                                                               local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path
            elif user and password:
                exec_shell("mongodump -u {user} -p {password} -h {cluster_ip} -o {local_path}"
                           .format(user=user, password=password, cluster_ip=cluster_ip, local_path=local_backup_path))
                exec_shell("tar zcvf {local_ok_path} {local_path}"
                           .format(local_ok_path=local_backup_file_path, local_path=local_backup_path))
                backup_path = local_backup_file_path[1:]
                return local_backup_file_path, backup_path

    def redis_backup(self):
        print("redisrest")


if __name__ == '__main__':
    print("test")