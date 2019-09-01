#!python
# -*- coding:utf-8 -*-

"""
类型转换函数的测试类
"""
import time
import datetime
import unittest

from JTL import type_change


class TestTypeChange(unittest.TestCase):

    def test_enum_file_change(self):
        """enum_file_change 测试"""
        file_name = 'tests/example_enum.json'

        self.assertEqual(type_change.enum_file_change('2', file_name), '离异')
        self.assertEqual(len(type_change.BIG_ENUM_JSON), 1)
        enum_dict = type_change.BIG_ENUM_JSON.get(file_name)
        self.assertEqual(enum_dict.get(1), None)

        self.assertEqual(type_change.enum_file_change(1, file_name), '已婚')
        self.assertEqual(len(type_change.BIG_ENUM_JSON), 1)
        enum_dict2 = type_change.BIG_ENUM_JSON.get(file_name)
        self.assertEqual(id(enum_dict), id(enum_dict2))
        self.assertEqual(enum_dict2.get(1), '已婚')

        self.assertEqual(enum_dict.get("未婚"), None)
        self.assertEqual(type_change.enum_file_change("未婚", file_name), "未婚")
        enum_dict2 = type_change.BIG_ENUM_JSON.get(file_name)
        self.assertEqual(id(enum_dict), id(enum_dict2))
        self.assertEqual(enum_dict2.get("未婚"), "未婚")

        self.assertEqual(type_change.enum_file_change("4", file_name), "丧偶")
        self.assertEqual(type_change.enum_file_change(5, file_name), None)
        self.assertEqual(type_change.enum_file_change('10', file_name), None)

    def test_enum_change(self):
        """enum_change 测试"""
        self.assertEqual(type_change.enum_change(1, {1: '一', 2: '二', 3: '三'}), '一')
        self.assertEqual(type_change.enum_change('3', {1: '一', 2: '二', 3: '三'}), '三')
        self.assertEqual(type_change.enum_change(1, {'1': '一', '2': '二', '3': '三'}), '一')
        self.assertEqual(type_change.enum_change('2', {'1': '一', '2': '二', '3': '三'}), '二')
        self.assertEqual(type_change.enum_change('二', {1: '一', 2: '二', 3: '三'}), '二')
        self.assertEqual(type_change.enum_change(5, {'1': '一', '2': '二', '3': '三'}), None)
        self.assertEqual(type_change.enum_change('10', {'1': '一', '2': '二', '3': '三'}), None)

    def test_date_2_str(self):
        """date_2_str 测试"""
        test_time = datetime.datetime(2019, 7, 6, 8, 51, 6)
        test_date = datetime.date(2019, 7, 29)

        self.assertEqual(type_change.date_2_str(None), None)
        self.assertEqual(type_change.date_2_str(''), None)
        self.assertEqual(type_change.date_2_str(test_date), '2019-07-29')
        self.assertEqual(type_change.date_2_str(test_time), '2019-07-06')
        self.assertEqual(type_change.date_2_str(time.localtime()), type_change.date_2_str(datetime.datetime.now()))
        self.assertEqual(type_change.date_2_str(time.time()), type_change.date_2_str(datetime.datetime.now()))
        self.assertEqual(type_change.date_2_str(test_date, format_str='%Y-%m-%d %H:%M:%S'), '2019-07-29 00:00:00')
        self.assertEqual(type_change.date_2_str(test_time, format_str='%Y-%m-%dT%H:%M:%S'), '2019-07-06T08:51:06')

    def test_datetime_2_str(self):
        """datetime_2_str 测试"""
        test_time = datetime.datetime(2019, 7, 6, 8, 51, 6)
        test_date = datetime.date(2019, 7, 29)

        self.assertEqual(type_change.datetime_2_str(None), None)
        self.assertEqual(type_change.datetime_2_str(''), None)
        self.assertEqual(type_change.datetime_2_str(test_date), '2019-07-29T00:00:00')
        self.assertEqual(type_change.datetime_2_str(test_time), '2019-07-06T08:51:06')
        self.assertEqual(type_change.datetime_2_str(time.localtime()),
                         type_change.datetime_2_str(datetime.datetime.now()))
        self.assertEqual(type_change.datetime_2_str(time.time()), type_change.datetime_2_str(datetime.datetime.now()))
        self.assertEqual(type_change.datetime_2_str(test_date, format_str='%Y-%m-%d %H:%M:%S'), '2019-07-29 00:00:00')
        self.assertEqual(type_change.datetime_2_str(test_time, format_str='%Y-%m-%dT%H:%M:%S'), '2019-07-06T08:51:06')

    def test_concat(self):
        """concat 测试"""
        self.assertEqual(type_change.concat({'a': 11, 'b': 22, 33: 'aa'}, ['a', 33]), '11aa')
        self.assertEqual(type_change.concat({'a': 11, 'b': 22, 33: 'aa'}, ['a', 'b', 33]), '1122aa')
        self.assertEqual(type_change.concat({'a': 11, 'b': 22, 33: 'aa'}, ['a', 'b', 33], '-'), '11-22-aa')
        self.assertEqual(type_change.concat({'a': 11, 'b': 22, 33: 'aa'}, ['a', 'd', 'b']), '1122')

    def test_get_any(self):
        """get_any 测试"""
        self.assertEqual(type_change.get_any({'a': None, 'b': 22, 33: 'aa'}, ['a', 'b']), 22)
        self.assertEqual(type_change.get_any({'a': 0, 'b': None, 33: 'aa'}, ['a', 'b', 33]), 0)
        self.assertEqual(type_change.get_any({'a': False, 'b': None, 33: 'aa'}, ['a', 'b', 33]), False)
        self.assertEqual(type_change.get_any({'a': None, 'b': None, 33: 'aa'}, ['a', 'b', 33]), 'aa')
        self.assertEqual(type_change.get_any({'a': None, 'b': None}, ['a', 'b', 33]), None)

    def test_get_list(self):
        """get_list 测试"""
        self.assertEqual(type_change.get_list({'a': 11, 'b': 22, 33: 'aa'}, ['a', 33]), [11, 'aa'])
        self.assertEqual(type_change.get_list({'a': 11, 'b': 22, 33: 'aa'}, ['a', 'b', 33]), [11, 22, 'aa'])
        self.assertEqual(type_change.get_list({'a': 11, 'b': 22, 33: 'aa'}, ['a', 'd', 'b']), [11, 22])

    def test_jtl(self):
        """jtl综合转换(无内嵌层)"""
        config_json = {
            "external_id": "user_id $ toString",
            "name": "name",
            "email": "email",
            "phone": "mobile_phone",
            "personal_id": "id_number",
            "age": "age",
            "gender": {
                "_source_col_name": "gender",
                "_type_change": "enum_change",
                "enum_dict": {"0": "女", "1": "男"}
            },
            "ethnicity": "nation",
            "nationality": "nationality",
            "year_of_work_experience": "work_year $ toInt",
            "birthday": {
                "_source_col_name": "birthday",
                "_type_change": "date_2_str",
                "format_str": "%Y/%m/%d"
            },
            "birthplace": "hometown",
            "marital_status": {
                "_source_col_name": "marital_status",
                "_type_change": "enum_file_change",
                "file_name": "tests/example_enum.json"
            },
            "update_dt": {
                "_source_col_name": "update_dt",
                "_type_change": "datetime_2_str",
            },
            "update_dt2": "update_dt $ toString",  # 日期转字符串，如果是默认格式可以直接用 toString 函数
            "summary": "description",
            "description2": '',  # 没有对应key，返回None
            'is_similar_check': False,  # 对应key不是字符串，原样返回
        }
        db_data = {
            'user_id': 111997,
            'name': '陈治卫',
            'age': 22,
            'birthday': datetime.date(1995, 7, 1),
            'gender': 0,
            'email': 'sdsa@qq.com',
            'mobile_phone': '13345678901',
            'marital_status': '2',
            'work_year': '7',
            'current_city': '辽宁省朝阳市友谊大街四段 (邮编：122000)',
            'height': None,
            'weight': None,
            'id_type': None,
            'id_number': '54557576',
            'photo': None,
            'nationality': None,
            'nation': None,
            'hometown': None,
            'update_dt': datetime.datetime(2019, 8, 5, 16, 13, 58),
            'description': '在校期间担任过班干部、学生会主席等，具有一定的组织协调能力。'
        }
        result = {
            'external_id': '111997',
            'name': '陈治卫',
            'email': 'sdsa@qq.com',
            'phone': '13345678901',
            'personal_id': '54557576',
            'age': 22,
            'gender': '女',
            'ethnicity': None,
            'nationality': None,
            'year_of_work_experience': 7,
            'birthday': '1995/07/01',
            'birthplace': None,
            'marital_status': "离异",
            'update_dt': '2019-08-05T16:13:58',
            'update_dt2': '2019-08-05T16:13:58',
            'summary': '在校期间担任过班干部、学生会主席等，具有一定的组织协调能力。',
            'description2': None,
            'is_similar_check': False,
        }
        self.assertEqual(type_change.jtl_change(db_data, config_json), result)

    def test_jtl2(self):
        """jtl综合转换(二层内嵌)"""
        config_json = {
            "name": "name",
            'educations': {
                "_source_col_name": "educations2",
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
        db_data = {
            'name': '陈治卫',
            'educations2': [{
                'start_date': datetime.date(2014, 9, 1),
                'end_date': datetime.date(2017, 6, 1),
                'school_name': '荆州理工职业学院',
                'education': 3,
                'major': '计算机应用技术',
                'education_mode': None,
                'max_education': 1
            }, {
                'start_date': datetime.date(2010, 9, 1),
                'end_date': datetime.date(2014, 6, 1),
                'school_name': '深圳大学',
                'education': 4,
                'major': '英语',
                'education_mode': None,
                'max_education': 1
            }],
            "skills": [{
                'skill_type': '计算机初级证书',
                'time_use': None,
                'compet_level': None
            }]
        }
        result = {
            'name': '陈治卫',
            'educations': [{
                'school_name': '荆州理工职业学院',
                'major': '计算机应用技术',
                'degree': '本科',
                'start_date': '2014-09-01',
                'end_date': '2017-06-01'
            }, {
                'school_name': '深圳大学',
                'major': '英语',
                'degree': '硕士及以上',
                'start_date': '2010-09-01',
                'end_date': '2014-06-01'
            }],
            'skills': [{
                'skill_category': None,
                'skill_name': '计算机初级证书',
                'skill_level': None
            }]

        }
        self.assertEqual(type_change.jtl_change(db_data, config_json), result)

    def test_jtl3(self):
        """jtl综合转换(三层内嵌)"""
        config_json = {
            "name": "name",
            # 第二层
            'educations': {
                "_source_col_name": "educations2",
                "_type_change": "list",
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
                    },
                    # 第三层
                    'skills22': {
                        "_source_col_name": "skills11",
                        "_type_change": "list",
                        "config_json": {
                            "skill_category": {
                                "_source_col_name": "*",
                                "_type_change": "concat",
                                "source_cols": ['skill_type', 'compet_level', 'time_use'],
                                'separator': '-'
                            },
                            "skill_name": "skill_type",
                            "skill_level": "compet_level"
                        }
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
        db_data = {
            'name': '陈治卫',
            'educations2': [{
                'start_date': datetime.date(2014, 9, 1),
                'end_date': datetime.date(2017, 6, 1),
                'school_name': '荆州理工职业学院',
                'education': 3,
                'major': '计算机应用技术',
                'education_mode': None,
                'max_education': 1
            }, {
                'start_date': datetime.date(2010, 9, 1),
                'end_date': datetime.date(2014, 6, 1),
                'school_name': '深圳大学',
                'education': 4,
                'major': '英语',
                'education_mode': None,
                'max_education': 1,
                "skills11": [{
                    'id': 1437,
                    'user_id': 111998,
                    'skill_type': '计算机水平考试一级证书',
                    'time_use': None,
                    'compet_level': '计算机水平一级'
                }, {
                    'id': 1445,
                    'user_id': 111999,
                    'skill_type': 'java',
                    'time_use': None,
                    'compet_level': '熟练'
                }]
            }],
            "skills": [{
                'skill_type': '计算机初级证书',
                'time_use': None,
                'compet_level': None
            }, {
                'id': 1437,
                'user_id': 111998,
                'skill_type': '计算机水平考试一级证书',
                'time_use': None,
                'compet_level': '计算机水平一级'
            }, {
                'id': 1445,
                'user_id': 111999,
                'skill_type': 'java',
                'time_use': None,
                'compet_level': '熟练'
            }]
        }
        result = {
            'name': '陈治卫',
            'educations': [{
                'school_name': '荆州理工职业学院',
                'major': '计算机应用技术',
                'degree': '本科',
                'start_date': '2014-09-01',
                'end_date': '2017-06-01',
                'skills22': None
            }, {
                'school_name': '深圳大学',
                'major': '英语',
                'degree': '硕士及以上',
                'start_date': '2010-09-01',
                'end_date': '2014-06-01',
                'skills22': [{
                    'skill_category': '计算机水平考试一级证书-计算机水平一级-',
                    'skill_name': '计算机水平考试一级证书',
                    'skill_level': '计算机水平一级'
                }, {
                    'skill_category': 'java-熟练-',
                    'skill_name': 'java',
                    'skill_level': '熟练'
                }]
            }],
            'skills': [{
                'skill_category': None,
                'skill_name': '计算机初级证书',
                'skill_level': None
            }, {
                'skill_category': None,
                'skill_name': '计算机水平考试一级证书',
                'skill_level': '计算机水平一级'
            }, {
                'skill_category': None,
                'skill_name': 'java',
                'skill_level': '熟练'
            }]
        }
        # print(type_change.jtl_change(db_data, config_json))
        # print(result)
        self.assertEqual(type_change.jtl_change(db_data, config_json), result)
        # 多检测一遍，确保输入数据源不会被修改
        self.assertEqual(type_change.jtl_change(db_data, config_json), result)


if __name__ == "__main__":
    unittest.main()
