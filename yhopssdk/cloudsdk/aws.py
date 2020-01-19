#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
author : Yehe
date   : 2020/1/18 16:42
role   : Aws boto3 方法
"""
import boto3


class PushS3(object):
    def __init__(self, data):
        """
        传入一个字典
        文件备份到S3上
        :param data: 传入的字典信息
        """
        self.aws_access_key_id = data.AWS_ACCESS_KEY_ID  # Aws Access_key ID
        self.aws_secret_access_key = data.AWS_SECRET_ACCESS_KEY  # Aws Access_key 密钥
        self.region_name = data.REGION_NAME  # Bucket区域
        self.bucket_name = data.BUCKET_NAME  # Bucket名字
        self.local_path = data.LOCAL_PATH  # 本地备份文件的路径
        self.backup_path = data.BACKUP_PATH  # 备份到AWS上的路径
        session = boto3.session.Session(region_name=self.region_name, aws_access_key_id=self.aws_access_key_id,
                        aws_secret_access_key=self.aws_secret_access_key)
        self.s3_init = session.resource('s3', self.region_name)
        self.s3 = self.s3_init.Bucket(self.bucket_name)

    def upload_file(self):
        try:
            self.s3.upload_file(self.local_path, self.backup_path)
        except Exception as ex:
            exit(ex)