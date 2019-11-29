# -*- coding:utf-8 -*-
"""
change type
"""

import uuid
import types
import time
import datetime
from JTL import Interpreter
from JTL import time_util
from JTL import Functions
from JTL.json_util import enum_change, enum_or_key, enum_file_change, decode2str
from JTL.time_util import to_date, to_datetime


__all__ = ('enum_change', 'enum_or_key', 'enum_file_change', 'date_2_str', 'datetime_2_str',
           'to_date', 'to_datetime', 'jtl_change')

DEFAULT_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'


@Functions.registerMaybeFunction('toString')
def to_string(data):
    """change input to string"""
    # time, datetime
    if isinstance(data, (datetime.datetime, time.struct_time)):
        return datetime_2_str(data)
    # date
    elif isinstance(data, datetime.date):
        return date_2_str(data)
    # datetime.time
    elif isinstance(data, datetime.time):
        return time_util.to_string(data)
    # uuid
    elif isinstance(data, uuid.UUID):
        return data.hex
    # bytes
    if isinstance(data, (bytes, bytearray)):
        return decode2str(data)
    return str(data)


@Functions.registerFunction('dateToString')
def date_2_str(value, format_str=None, default_now=False):
    """
    change a time to string
    :param {time|datetime.datetime|datetime.date|int|long|float|string} value: original time
    :param {string} format_str: the return format of time. (default format: %Y-%m-%d)
    :param {bool} default_now: True: when value is None return now, False: when value is None return None.
    :return {string}: the string time

    use in JTL: '<SELECTOR> $ dateToString "<format_str>" '
    """
    format_str = format_str or DEFAULT_DATE_FORMAT
    return time_util.to_string(value, format_str, default_now=default_now)


@Functions.registerFunction('datetimeToString')
def datetime_2_str(value, format_str=None, default_now=False):
    """
    change a time to string
    :param {time|datetime.datetime|datetime.date|int|long|float|string} value: original time
    :param {string} format_str: the return format of time. (default format: %Y-%m-%dT%H:%M:%S)
    :param {bool} default_now: True: when value is None return now, False: when value is None return None.
    :return {string}: the string time

    use in JTL: '<SELECTOR> $ datetimeToString "<format_str>" '
    """
    format_str = format_str or DEFAULT_TIME_FORMAT
    return date_2_str(value, format_str=format_str, default_now=default_now)


# register functions of date
Functions.register('toDate', time_util.to_date)
Functions.register('toDatetime', time_util.to_datetime)


def jtl_change(data, config_json):
    """
    将数据库读取的数据，经过 JTL 转换(支持多层内嵌)
    :param data: 源数据
    :param config_json: 数据映射的配置dict
    :return:

    json配置范例(读取内嵌层):
        config_json = {
            "name": "name",
            'educations': {
                "_source_col_name": "educations",
                "_type_change": "jtl_change",
                "config_json": {
                    "school_name": "school_name",
                    "major": "major",
                    "degree": {
                        "_source_col_name": "education",
                        "_type_change": "enum_change",
                        "enum_dict": {"1": "高中及以下", "2": "大专", "3": "本科", "4": "硕士及以上"}
                    },
                    "start_date": {
                        "_source_col_name": "start_date",
                        "_type_change": "date_2_str"
                    },
                    "end_date": {
                        "_source_col_name": "end_date",
                        "_type_change": "date_2_str"
                    }
                }
            },
            'skills': {
                "_source_col_name": "skills",
                "_type_change": "jtl_change",
                "config_json": {
                    "skill_category": "",
                    "skill_name": "skill_type",
                    "skill_level": "compet_level"
                }
            }
        }
    """
    if data is None:
        return None

    # 经 JTL 转码数据的配置
    transform_data = {}
    for k, v in config_json.items():
        # 自定义转换函数
        if isinstance(v, dict) and v.get('_source_col_name') and v.get('_type_change'):
            v_param = v.copy()  # 避免改变原配置
            _source_col_name = v_param.pop('_source_col_name')
            _type = v_param.pop('_type_change')
            fun = lambda *args, **kwargs: None
            if isinstance(_type, str):
                if _type in __all__:
                    fun = eval(_type)
                elif _type in Functions.functions:
                    fun = Functions.functions.get(_type)
            elif isinstance(_type, (types.FunctionType, types.MethodType)):
                fun = _type
            param = (_source_col_name, fun, v_param)
            transform_data[k] = param
        # jtl 的转换
        else:
            transform_data[k] = v

    if isinstance(data, dict):
        return Interpreter.transformJson(data, transform_data)
    elif isinstance(data, (tuple, list)):
        return [jtl_change(d, transform_data) for d in data]
    return data


@Functions.registerFunction('countAge')
def count_age(data, key):
    """
    count age by birth_date
    """
    birth_date = data.get(key)
    if not birth_date:
        return None
    birth_date = to_date(birth_date)
    now = datetime.date.today()
    if birth_date > now:
        return None
    timedelta = now - birth_date
    return int(timedelta.days / 365.25)
