# -*- coding:utf-8 -*-
"""
change type
"""

import time
import datetime
from JTL import Interpreter, time_util

__all__ = ('date_2_str', 'datetime_2_str', 'jtl_change')


def date_2_str(value, format_str='%Y-%m-%d', default_now=False):
    """
    将日期格式化成字符串
    :param {time|datetime.datetime|datetime.date|int|float|str} value: 原时间(纯数值则认为是时间戳,单位:秒)
    :param {string} format_str: 期望返回结果的格式字符串(默认为: %Y/%m/%d)
    :param {string} default_now: 为 True 时当 value 是空值返回当前时间。为 False 时当 value 是空值返回 None。
    :return {string}: 格式化后的时间字符串

    数据库配置范例:
        db.getCollection("trans_fields").insert( {
            "external_name": "shunfeng",
            "bello_field": "birthday",
            "external_field": "birthday",
            "description": "生日",
            "to_bello_fun": "date_2_str",
            "to_bello_param": null,  // 参数跟默认值一样的话可以设参数为空值
            "to_external_fun": "date_2_str",
            "to_external_param": {"format_str": "%Y-%m-%d"}
        } );
    json配置范例:
        {"birthday": {
            "_source_col_name": "birthday",
            "_type_change": "date_2_str",
            "format_str": "%Y/%m/%d"
          },
          "start_date": {
            "_source_col_name": "start_date",
            "_type_change": "date_2_str",  # 参数跟默认值一样的话可以不写参数
          },
          "end_date": "end_date $ toString"  # 日期转字符串，如果是默认格式可以直接用 toString 函数，它会根据 datetime.datetime 及 datetime.date 类型来判断格式
        }
    """
    format_str = format_str or '%Y-%m-%d'
    return time_util.to_string(value, format_str, default_now=default_now)


def datetime_2_str(value, format_str='%Y-%m-%dT%H:%M:%S', default_now=False):
    """
    将日期格式化成字符串
    :param {time|datetime.datetime|datetime.date|int|float|str} value: 原时间(纯数值则认为是时间戳,单位:秒)
    :param {string} format_str: 期望返回结果的格式字符串(默认为: %Y/%m/%dT%H:%M:%S)
    :param {string} default_now: 为 True 时当 value 是空值返回当前时间。为 False 时当 value 是空值返回 None。
    :return {string}: 格式化后的时间字符串

    数据库配置范例:
        db.getCollection("trans_fields").insert( {
            "external_name": "shunfeng",
            "bello_field": "end_date",
            "external_field": "end_date",
            "description": "结束时间",
            "to_bello_fun": "datetime_2_str",
            "to_bello_param": null,  // 参数跟默认值一样的话可以设参数为空值
            "to_external_fun": "datetime_2_str",
            "to_external_param": {"format_str": "%Y-%m-%d %H:%M:%S"}
        } );
    json配置范例:
        {"birthday": {
            "_source_col_name": "birthday",
            "_type_change": "datetime_2_str",
            "format_str": "%Y/%m/%d %H:%M:%S"
          },
          "start_date": {
            "_source_col_name": "start_date",
            "_type_change": "datetime_2_str",  # 参数跟默认值一样的话可以不写参数
          },
          "end_date": "end_date $ toString"  # 日期转字符串，如果是默认格式可以直接用 toString 函数，它会根据 datetime.datetime 及 datetime.date 类型来判断格式
        }
    """
    format_str = format_str or '%Y-%m-%dT%H:%M:%S'
    return date_2_str(value, format_str=format_str, default_now=default_now)


def to_date(value, default_now=False):
    """
    将 字符串或者其它类型的时间 转成 datetime.date 类型
    :param {time|datetime.datetime|datetime.date|int|float|str} value: 原时间(纯数值则认为是时间戳,单位:秒)
    :param {string} format_str: 期望返回结果的格式字符串(默认为: %Y/%m/%d)
    :param {bool} default_now: 为 True 时当 value 是空值返回当前时间。为 False 时当 value 是空值返回 None。
    :return {datetime.date}: 对应的日期

    数据库配置范例:
        db.getCollection("trans_fields").insert( {
            "external_name": "shunfeng",
            "bello_field": "birthday",
            "external_field": "birthday",
            "description": "生日",
            "to_bello_fun": "date_2_str",
            "to_bello_param": null,  // 参数跟默认值一样的话可以设参数为空值
            "to_external_fun": "to_date",
            "to_external_param": {"format_str": "%Y-%m-%d", "default_now": true}
        } );
    json配置范例:
        {"birthday": {
            "_source_col_name": "birthday",
            "_type_change": "to_date",
            "format_str": "%Y/%m/%d",
            "default_now": True
          },
          "start_date": {
            "_source_col_name": "start_date",
            "_type_change": "to_date",  # 参数跟默认值一样的话可以不写参数
          }
        }
    """
    return time_util.to_date(value, default_now=default_now)


def to_datetime(value, default_now=False):
    """
    将 字符串或者其它类型的时间 转成 datetime.datetime 类型
    :param {time|datetime.datetime|datetime.date|int|float} value: 原时间(纯数值则认为是时间戳,单位:秒)
    :param {string} format_str: 期望返回结果的格式字符串(默认为: %Y/%m/%dT%H:%M:%S)
    :param {bool} default_now: 为 True 时当 value 是空值返回当前时间。为 False 时当 value 是空值返回 None。
    :return {string}: 格式化后的时间字符串

    数据库配置范例:
        db.getCollection("trans_fields").insert( {
            "external_name": "shunfeng",
            "bello_field": "end_date",
            "external_field": "end_date",
            "description": "结束时间",
            "to_bello_fun": "to_datetime",
            "to_bello_param": null,  // 参数跟默认值一样的话可以设参数为空值
            "to_external_fun": "to_datetime",
            "to_external_param": {"format_str": "%Y-%m-%d %H:%M:%S", "default_now": true}
        } );
    json配置范例:
        {"birthday": {
            "_source_col_name": "birthday",
            "_type_change": "to_datetime",
            "format_str": "%Y/%m/%d %H:%M:%S",
            "default_now": True
          },
          "start_date": {
            "_source_col_name": "start_date",
            "_type_change": "to_datetime",  # 参数跟默认值一样的话可以不写参数
          }
        }
    """
    return time_util.to_datetime(value, default_now=default_now)


def jtl_change(data, config_json):
    """
    将数据库读取的数据，经过 JTL 转换(支持多层内嵌)
    :param data: 源数据
    :param config_json: 数据映射的配置dict
    :return:

    数据库配置范例:
        db.getCollection("trans_fields").insert( {
            "external_name": "shunfeng",
            "bello_field": "start_date",
            "external_field": "start_date",
            "description": "开始日期",
            "external_parent": "educations",  // 必须配置对应的父级名称
            "bello_parent": "educations",  // 必须配置对应的父级名称
            "to_bello_fun": "date_2_str",
            "to_bello_param": null,
            "to_external_fun": "date_2_str",
            "to_external_param": {"format_str": "%Y-%m-%d"}
        } );
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
            if _type in __all__:
                fun = eval(_type)
                param = (_source_col_name, fun, v_param)
                transform_data[k] = param
            # 处理内嵌list，还是由 jtl_change 统一处理，起个别名即可
            elif _type == 'list':
                transform_data[k] = (_source_col_name, jtl_change, v_param)
        # jtl 的转换
        else:
            transform_data[k] = v

    if isinstance(data, dict):
        return Interpreter.transformJson(data, transform_data)
    elif isinstance(data, (tuple, list)):
        return [jtl_change(d, transform_data) for d in data]
    return data
