# -*- coding:utf-8 -*-
"""
change type
"""

import types
from JTL import Interpreter
from JTL import time_util
from JTL import Functions


__all__ = ('date_2_str', 'datetime_2_str', 'jtl_change')


def date_2_str(value, format_str='%Y-%m-%d', default_now=False):
    """
    change a time to string
    :param {time|datetime.datetime|datetime.date|int|long|float|string} value: original time
    :param {string} format_str: the return format of time. (default format: %Y-%m-%d)
    :param {bool} default_now: True: when value is None return now, False: when value is None return None.
    :return {string}: the string time
    """
    format_str = format_str or '%Y-%m-%d'
    return time_util.to_string(value, format_str, default_now=default_now)


def datetime_2_str(value, format_str='%Y-%m-%dT%H:%M:%S', default_now=False):
    """
    change a time to string
    :param {time|datetime.datetime|datetime.date|int|long|float|string} value: original time
    :param {string} format_str: the return format of time. (default format: %Y-%m-%dT%H:%M:%S)
    :param {bool} default_now: True: when value is None return now, False: when value is None return None.
    :return {string}: the string time
    """
    format_str = format_str or '%Y-%m-%dT%H:%M:%S'
    return date_2_str(value, format_str=format_str, default_now=default_now)


Functions.functions.update({
    # Date
    'dateToString': date_2_str,
    'datetimeToString': datetime_2_str,
    'toDate': time_util.to_date,
    'toDatetime': time_util.to_datetime,
})


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
                        "_type_change": "enumChange",
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
