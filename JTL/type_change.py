#!python
# -*- coding:utf-8 -*-
"""
类型转换函数
"""
import os
import time
import datetime
from JTL.Interpreter import transformJson
from . import json_util

__all__ = ('enum_change', 'enum_change', 'enum_file_change', 'date_2_str', 'datetime_2_str', 'concat', 'get_list',
           'get_any', 'jtl_change')

# 大json形式的枚举，缓存起它的值
BIG_ENUM_JSON = {}


def enum_file_change(value, file_name):
    """枚举值转换
    :param value: 枚举的key
    :param file_name: 枚举映射表路径(要求是json文件,且放在项目下的 trans_json 目录)
    :return: 映射表里对应的值

    数据库配置范例:
        db.getCollection("trans_fields").insert( {
            "external_name": "shunfeng",
            "bello_field": "marital_status",
            "external_field": "marital_status",
            "description": "婚姻状态",
            "to_bello_fun": "enum_file_change",
            "to_bello_param": {"file_name": "example_enum.json"},
            "to_external_fun": "enum_change",
            "to_external_param": {"未婚": "0", "已婚": "1", "离异": "2"}
        } );
    json配置范例:
        {"marital_status": {
            "_source_col_name": "marital_status",
            "_type_change": "enum_file_change",
            "file_name": "example_enum.json"
        }}
    """
    global BIG_ENUM_JSON
    if file_name in BIG_ENUM_JSON:
        enum_dict = BIG_ENUM_JSON.get(file_name)
    else:
        if file_name.startswith('/'):
            file_path = file_name
        else:
            file_path = os.path.join(os.getcwd(), file_name)
        enum_dict = json_util.load_json_file(file_path)
        assert isinstance(enum_dict, dict)
        BIG_ENUM_JSON[file_name] = enum_dict

    if value in enum_dict:
        return enum_dict.get(value)
    if isinstance(value, str):
        if value.isdigit():
            tem_value = int(value)
            if tem_value in enum_dict:
                target = enum_dict.get(tem_value)
                enum_dict[value] = target
                return target
    else:
        tem_value = str(value)
        if tem_value in enum_dict:
            target = enum_dict.get(tem_value)
            enum_dict[value] = target
            return target
    if value in enum_dict.values():
        enum_dict[value] = value
        return value
    enum_dict[value] = None
    return None


def enum_change(value, enum_dict):
    """枚举值转换
    :param value: 枚举的key
    :param enum_dict: 枚举映射表
    :return: 映射表里对应的值

    数据库配置范例:
        db.getCollection("trans_fields").insert( {
            "external_name": "huawei",
            "bello_field": "gender",
            "external_field": "TITLE",
            "description": "性别",
            "to_bello_fun": "enum_change",
            "to_bello_param": {"enum_dict": {"F": "女", "M": "男"}},
            "to_external_fun": "enum_change",
            "to_external_param": {"enum_dict": {"女": "F", "男": "M"}}
        } );
    json配置范例:
        {"degree": {
            "_source_col_name": "education",
            "_type_change": "enum_change",
            "enum_dict": {"1": "高中及以下", "2": "大专", "3": "本科", "4": "硕士及以上"}
        }}
    """
    if value in enum_dict:
        return enum_dict.get(value)
    if isinstance(value, str):
        if value.isdigit():
            tem_value = int(value)
            if tem_value in enum_dict:
                return enum_dict.get(tem_value)
    else:
        tem_value = str(value)
        if tem_value in enum_dict:
            return enum_dict.get(tem_value)
    if value in enum_dict.values():
        return value
    return None


def date_2_str(value, format_str='%Y-%m-%d'):
    """
    将日期格式化成字符串
    :param {time|datetime.datetime|datetime.date|int|float} value: 原时间(为空则默认为当前时间；纯数值则认为是时间戳,单位:秒)
    :param {string} format_str: 期望返回结果的格式字符串(默认为: %Y/%m/%d)
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
    if value in (None, ''):
        return None

    format_str = format_str or '%Y-%m-%d'
    # datetime, datetime.date
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.strftime(format_str)
    # time
    elif isinstance(value, time.struct_time):
        return time.strftime(format_str, value)
    # 纯数值类型, 先类型转换
    elif isinstance(value, (int, float)):
        value = datetime.datetime.fromtimestamp(value)
        return value.strftime(format_str)
    # 其它类型,无法格式化
    return None


def datetime_2_str(value, format_str='%Y-%m-%dT%H:%M:%S'):
    """
    将日期格式化成字符串
    :param {time|datetime.datetime|datetime.date|int|float} value: 原时间(为空则默认为当前时间；纯数值则认为是时间戳,单位:秒)
    :param {string} format_str: 期望返回结果的格式字符串(默认为: %Y/%m/%dT%H:%M:%S)
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
    return date_2_str(value, format_str=format_str)


def concat(data, source_cols=None, separator=''):
    """
    合并多个字段值
    :param {dict} data: 数据源
    :param {list} source_cols: 要合并的字段名列表(是数据源的字段名，而不是转换后的字段名)
    :param {str} separator: 分隔符
    :return: 合并后的字符串

    数据库配置范例:
        db.getCollection("trans_fields").insert( {
            "external_name": "shunfeng",
            "bello_field": "skill_category",
            "external_field": "*", // 由于需要读取多个字段，所以没法指定具体某个字段名，这里必须填 "*"
            "description": "技能",
            "to_bello_fun": "concat",
            "to_bello_param": {"source_cols": ["skill_type", "compet_level", "time_use"], "separator": "-"},
            "to_external_fun": null,
            "to_external_param": null
        } );
    json配置范例:
        {"skill_category": {
                "_source_col_name": "*",
                "_type_change": "concat",
                "source_cols": ['skill_type', 'compet_level', 'time_use'],
                'separator': '-'
            }
        }
    """
    if data is None:
        return None
    if not source_cols:
        return ''

    assert isinstance(source_cols, (list, tuple))
    results = [str(data.get(i, '') or '') for i in source_cols]
    return separator.join(results)


def get_list(data, source_cols=None):
    """
    获取多个字段值，且以list形式返回
    (几乎是专门为我们简历model的 expected_locations(期望工作地点) 字段而写，因为它的类型是 ListField(StringField()) )
    :param {dict} data: 数据源
    :param {list} source_cols: 要获取的字段名列表(是数据源的字段名，而不是转换后的字段名)
    :return: 合并后的字符串

    数据库配置范例:
        db.getCollection("trans_fields").insert( {
            "external_name": "huawei",
            "bello_field": "expected_locations",
            "external_field": "*", // 由于需要读取多个字段，所以没法指定具体某个字段名，这里必须填 "*"
            "description": "期望工作地点",
            "to_bello_fun": "get_list",
            "to_bello_param": {"source_cols": ["INTENTION_PLACE", "INTENTION_PLACE_ONE", "INTENTION_PLACE_TWO"]}
        } );
    json配置范例:
        {"expected_locations": {
                "_source_col_name": "*",
                "_type_change": "get_list",
                "source_cols": ["INTENTION_PLACE", "INTENTION_PLACE_ONE", "INTENTION_PLACE_TWO"]
            }
        }
    """
    if data is None:
        return None
    if not source_cols:
        return []

    assert isinstance(source_cols, (list, tuple))
    return [data.get(i) for i in source_cols if data.get(i) is not None]


def get_any(data, source_cols=None):
    """
    在多个字段中，获取有值的任意一个，按字段列表的优先顺序取
    :param {dict} data: 数据源
    :param {list} source_cols: 要获取的字段名列表(是数据源的字段名，而不是转换后的字段名)
    :return: 对应字段的值,取不到时返回 None

    数据库配置范例:
        db.getCollection("trans_fields").insert( {
            "external_name": "shunfeng",
            "bello_field": "skill_category",
            "external_field": "*", // 由于需要读取多个字段，所以没法指定具体某个字段名，这里必须填 "*"
            "description": "技能",
            "to_bello_fun": "get_any",
            "to_bello_param": {"source_cols": ["skill_type", "compet_level", "time_use"]},
            "to_external_fun": null,
            "to_external_param": null
        } );
    json配置范例:
        {"skill_category": {
                "_source_col_name": "*",
                "_type_change": "get_any",
                "source_cols": ['skill_type', 'compet_level', 'time_use']
            }
        }
    """
    if data is None:
        return None
    if not source_cols:
        return ''

    assert isinstance(source_cols, (list, tuple))
    for i in source_cols:
        value = data.get(i)
        if value is not None:
            return value
    return None


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
        return transformJson(data, transform_data)
    elif isinstance(data, (tuple, list)):
        return [jtl_change(d, transform_data) for d in data]
    return data
