#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
author : Yehe
date   : 2020/1/18 16:39
role   : 执行shall命令
"""

import subprocess


def exec_shell(cmd):
    """
    执行shell命令函数
    :param cmd:
    :return:
    """
    sub2 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = sub2.communicate()
    ret = sub2.returncode
    return ret, stdout.decode('utf-8').strip()