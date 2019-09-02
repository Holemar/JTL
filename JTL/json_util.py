# -*- coding:utf-8 -*-
"""
json Utility
"""
import os
import sys
import json
import uuid
import time
import datetime
import logging
import decimal

# base file path, for found files
BASE_PATH = os.getcwd()

# string encoding, try to encode str or decode bytes by this list
CODING_LIST = ('utf8', 'unicode-escape', sys.getdefaultencoding(), 'gbk', 'big5')

# enum file json cache
BIG_ENUM_JSON = {}


def decode2str(content):
    """change bytes to str"""
    if content is None:
        return None
    if isinstance(content, bytes):
        for encoding in CODING_LIST:
            try:
                return content.decode(encoding)
            except UnicodeDecodeError as e:
                pass
        # If that fails, ignore error messages
        content = content.decode("utf8", "ignore")
    return content


def encode2bytes(content):
    """change str to bytes"""
    if content is None:
        return None
    if isinstance(content, str):
        for encoding in CODING_LIST:
            try:
                return content.encode(encoding)
            except UnicodeEncodeError as e:
                pass
        # If that fails, ignore error messages
        content = content.encode('utf8', 'ignore')
    return content


def enum_file_change(key, file_name):
    """big enum json load by a file
    :param key: key of enum json
    :param file_name: the file of enum json
    :return: value of enum json
    """
    global BIG_ENUM_JSON
    if file_name in BIG_ENUM_JSON:
        enum_dict = BIG_ENUM_JSON.get(file_name)
    else:
        enum_dict = load_json_file(file_name)
        assert isinstance(enum_dict, dict)
        BIG_ENUM_JSON[file_name] = enum_dict

    if key in enum_dict:
        return enum_dict.get(key)

    if isinstance(key, str):
        if key.isdigit():
            tem_value = int(key)
            if tem_value in enum_dict:
                target = enum_dict.get(tem_value)
                enum_dict[key] = target
                return target
    else:
        tem_value = str(key)
        if tem_value in enum_dict:
            target = enum_dict.get(tem_value)
            enum_dict[key] = target
            return target

    if key in enum_dict.values():
        enum_dict[key] = key
        return key

    enum_dict[key] = None
    return None


def enum_change(key, enum_dict):
    """get the value of enum
    :param key: key of enum json
    :param enum_dict: enum json
    :return: value of enum json
    """
    if isinstance(enum_dict, str):
        enum_dict = load_json(enum_dict)
        assert isinstance(enum_dict, dict)

    if key in enum_dict:
        return enum_dict.get(key)

    if isinstance(key, str):
        if key.isdigit():
            tem_value = int(key)
            if tem_value in enum_dict:
                return enum_dict.get(tem_value)
    else:
        tem_value = str(key)
        if tem_value in enum_dict:
            return enum_dict.get(tem_value)

    if key in enum_dict.values():
        return key
    return None


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
    if not os.path.isfile(file_path):
        if file_path.startswith('/'):
            return None
        else:
            file_path = os.path.join(BASE_PATH, file_path)
            if not os.path.isfile(file_path):
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
    # list,tuple,set recursion
    elif isinstance(value, (list, tuple, set)):
        arr = [json_serializable(item) for item in value]
        return arr
    # dict recursion(the key in dict will change to str too)
    elif isinstance(value, dict):
        this_value = {}  # do not change the type
        for key1, value1 in value.items():
            key1 = json_serializable(key1)
            this_value[key1] = json_serializable(value1)
        return this_value
    else:
        return str(value)


def dump_json_file(json_value, file_path):
    """
    write json content to a file
    :param json_value: json content
    :param file_path: str
    :return: True if write success, else False
    """
    try:
        json_value = json_serializable(json_value)
        with open(file_path, 'w', encoding='utf-8') as dump_file:
            json.dump(json_value, dump_file, indent=1, ensure_ascii=False)
    except Exception as e:
        logging.error('write a json file error:%s', e, exc_info=True)
    return True

