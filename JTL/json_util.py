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
import base64
import logging
import decimal

# base file path, for found files
BASE_PATH = os.getcwd()

# string encoding, try to encode str or decode bytes by this list
DECODE_CODING_LIST = ['utf-8', 'gbk', 'gb2312', 'big5', 'gb18030']
ENCODE_CODING_LIST = ['gb2312', 'big5', 'gbk', 'gb18030', 'utf-8']
default_code = sys.getdefaultencoding()
if default_code not in DECODE_CODING_LIST:
    DECODE_CODING_LIST.append(default_code)
if default_code not in ENCODE_CODING_LIST:
    ENCODE_CODING_LIST[-1:-1] = [default_code]

# enum file json cache
BIG_ENUM_JSON = {}


def decode2str(content):
    """change str, bytes or bytearray to str"""
    if content is None:
        return None
    if isinstance(content, (bytes, bytearray)):
        try:
            return content.decode()
        # 特殊类型编码，尝试解码
        except UnicodeDecodeError as e:
            return to_utf8_str(content)
    return content


def encode2bytes(content):
    """change str to bytes"""
    if content is None:
        return None
    if isinstance(content, str):
        try:
            return content.encode()
        # 特殊类型编码，尝试解码
        except UnicodeEncodeError as e:
            return to_utf8_bytes(content)
    return content


def to_utf8_str(content):
    """change str, bytes or bytearray to utf-8 str"""
    if content is None:
        return None
    if isinstance(content, (bytes, bytearray)):
        # unicode-escape
        if '\\u' in str(content):
            try:
                return content.decode('unicode-escape').encode().decode()
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                pass
        # try code list
        for encoding in DECODE_CODING_LIST:
            try:
                value = content.decode(encoding)
                if encoding == 'utf-8':
                    return value
                else:
                    return value.encode().decode()  # change to utf-8 string
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                pass
        # If that fails, ignore error messages
        return content.decode("utf-8", "ignore")
    elif isinstance(content, str):
        # unicode-escape
        try_s = [ord(a) for a in content if ord(a) <= 256]
        if len(try_s) == len(content):
            return bytes(try_s).decode("utf-8")
        # try code list
        for encoding in ENCODE_CODING_LIST:
            try:
                value = content.encode(encoding)
                return value.decode()
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                pass
        # If that fails, ignore error messages
        return content.encode('utf-8', 'ignore').decode()
    return content


def to_utf8_bytes(content):
    """change str to utf-8 bytes"""
    if content is None:
        return None
    if isinstance(content, str):
        # unicode-escape
        try_s = [ord(a) for a in content if ord(a) <= 256]
        if len(try_s) == len(content):
            return bytes(try_s)
        # try code list
        for encoding in ENCODE_CODING_LIST:
            try:
                value = content.encode(encoding)
                if encoding == 'utf-8':
                    return value
                else:
                    return value.decode().encode()  # change to utf-8 bytes
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                pass
        # If that fails, ignore error messages
        content = content.encode('utf-8', 'ignore')
    return content


def base64_encode(s):
    """使用base64加密"""
    s = encode2bytes(s)
    res = base64.b64encode(s)
    return decode2str(res)


def base64_decode(s):
    """使用base64解码"""
    s = encode2bytes(s)
    res = base64.b64decode(s)
    return decode2str(res)


def enum_file_change(key, file_name):
    """big enum json load by a file
    :param key: key of enum json
    :param file_name: the file of enum json
    :return: value of enum json

    use in JTL: "<SELECTOR> $ enumFileChange '/data/example_enum.json' "
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
            tem_key = int(key)
            if tem_key in enum_dict:
                target = enum_dict.get(tem_key)
                enum_dict[key] = target
                return target
    else:
        tem_key = str(key)
        if tem_key in enum_dict:
            target = enum_dict.get(tem_key)
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

    use in JTL: '''<SELECTOR> $ enumChange '{"F": "女", "M": "男"}' '''
    """
    if isinstance(enum_dict, str):
        enum_dict = load_json(enum_dict)
        assert isinstance(enum_dict, dict)

    if key in enum_dict:
        return enum_dict.get(key)

    if isinstance(key, str):
        if key.isdigit():
            tem_key = int(key)
            if tem_key in enum_dict:
                return enum_dict.get(tem_key)
    else:
        tem_key = str(key)
        if tem_key in enum_dict:
            return enum_dict.get(tem_key)

    if key in enum_dict.values():
        return key
    return None


def enum_or_key(key, enum_dict):
    """get the value of enum, if not found then return the key
    :param key: key of enum json
    :param enum_dict: enum json
    :return: value of enum json, if not found in the enum then return the key

    use in JTL: '''<SELECTOR> $ enumOrKey '{"F": "女", "M": "男"}' '''
    """
    if isinstance(enum_dict, str):
        enum_dict = load_json(enum_dict)
        assert isinstance(enum_dict, dict)

    if key in enum_dict:
        return enum_dict.get(key)

    if isinstance(key, str):
        if key.isdigit():
            tem_key = int(key)
            if tem_key in enum_dict:
                value = enum_dict.get(tem_key)
                enum_dict[key] = value
                return value
    else:
        tem_key = str(key)
        if tem_key in enum_dict:
            value = enum_dict.get(tem_key)
            enum_dict[key] = value
            return value

    enum_dict[key] = key
    return key


def load_json(value):
    """
    change strings to json
    :param value: string
    :return: json dict
    """
    if value is None:
        return None

    if isinstance(value, (bytes, bytearray)):
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
    elif isinstance(value, (bytes, bytearray)):
        return decode2str(value)
    # str/unicode
    elif isinstance(value, str):
        return value
    elif isinstance(value, (bool, int, float, complex)):
        return value
    # time, datetime to str
    elif isinstance(value, time.struct_time):
        return time.strftime('%Y-%m-%dT%H:%M:%S', value)
    elif isinstance(value, datetime.datetime):
        return value.strftime('%Y-%m-%dT%H:%M:%S')
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


class CustomJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """
    def default(self, o):
        return json_serializable(o)


def dump_json_file(json_value, file_path):
    """
    write json content to a file
    :param json_value: json content
    :param file_path: str
    :return: True if write success, else False
    """
    try:
        json_value = json_serializable(json_value)
        # 没有文件的目录，则先创建目录，避免因此报错
        file_dir = os.path.dirname(file_path)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        with open(file_path, 'w', encoding='utf-8') as dump_file:
            json.dump(json_value, dump_file, indent=1, ensure_ascii=False)
    except Exception as e:
        logging.error('write a json file error:%s', e, exc_info=True)
    return True

