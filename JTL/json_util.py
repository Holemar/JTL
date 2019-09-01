# -*- coding:utf-8 -*-
"""
json Utility
"""
import os
import json
import uuid
import time
import datetime
import logging
import decimal


def decode2str(content):
    """change bytes to str"""
    if not content:
        return None
    if isinstance(content, bytes):
        for encoding in ('utf-8', 'gbk', 'big5', sys.getdefaultencoding(), 'unicode-escape'):
            try:
                return content.decode(encoding)
            except UnicodeDecodeError as e:
                pass
        # If that fails, ignore error messages
        content = content.decode("utf8", "ignore")
    return content


def load_json(value):
    """
    change strings to json
    :param value: string
    :return: json dict
    """
    if value is None:
        return None

    if isinstance(value, bytes):
        value = decode2str(value)
    if not isinstance(value, str):
        return None

    try:
        return json.loads(value)
    except ValueError as e:
        pass

    # Maybe that's a python value
    try:
        # fix json works: true, false, null ...
        true = True
        false = False
        null = None
        return eval(value)
    except Exception as e:
        return None


def load_json_file(file_path):
    """
    read file to json
    :param file_path: file path
    :return: json dict
    """
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as load_f:
        value = load_f.read()
        return load_json(value)
    return None


def json_serializable(value):
    """
    change the stings in (list, tuple, set, dict) to unicode
    :param value: dict,list,tuple,set
    :return {type(value)}:
    """
    if value is None:
        return None
    # str/unicode
    elif isinstance(value, str):
        return value
    elif isinstance(value, (bool, int, float, complex)):
        return value
    # time, datetime to str
    elif isinstance(value, time.struct_time):
        return time.strftime('%Y-%m-%d %H:%M:%S', value)
    elif isinstance(value, datetime.datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d')
    elif isinstance(value, decimal.Decimal):
        return float(value)
    elif isinstance(value, uuid.UUID):
        return value.hex
    # list,tuple,set 类型,递归转换
    elif isinstance(value, (list, tuple, set)):
        arr = [json_serializable(item) for item in value]
        return arr
    # dict 类型,递归转换(字典里面的 key 也会转成 unicode 编码)
    elif isinstance(value, dict):
        this_value = {}  # 不能改变原参数
        for key1, value1 in value.items():
            # 字典里面的 key 也转成 unicode 编码
            key1 = json_serializable(key1)
            this_value[key1] = json_serializable(value1)
        return this_value
    # 其它类型
    else:
        return str(value)


def dump_json_file(json_value, file_path):
    """
    将json内容写入到文件
    :param json_value: json内容
    :param file_path: 文件路径
    :return: 写入是否成功
    """
    try:
        json_value = json_serializable(json_value)
        with open(file_path, 'w', encoding='utf-8') as dump_file:
            json.dump(json_value, dump_file, indent=1, ensure_ascii=False)
    except Exception as e:
        logging.error('写入son文件异常:%s', e, exc_info=True)
    return True

