# -*- coding:utf-8 -*-
"""
type_change unittest
"""

import uuid
import time
import datetime
import unittest

from JTL import Interpreter
from JTL import type_change


class TestTypeChange(unittest.TestCase):

    def test_to_string(self):
        self.assertEqual(type_change.to_string(None), None)
        self.assertEqual(type_change.to_string(''), '')
        self.assertEqual(type_change.to_string(b'aa'), 'aa')
        self.assertEqual(type_change.to_string(uuid.UUID('409c7441-a4a5-4ce1-9b3c-c7e0002e87bd')),
                         '409c7441a4a54ce19b3cc7e0002e87bd')

        # time
        self.assertEqual(type_change.to_string(datetime.datetime(2019, 9, 3, 8, 51, 6)), '2019-09-03T08:51:06')
        self.assertEqual(type_change.to_string(datetime.date(2019, 9, 13)), '2019-09-13')
        dt = time.strptime('2014/03/25 19:05:33', '%Y/%m/%d %H:%M:%S')
        self.assertEqual(type_change.to_string(dt), '2014-03-25T19:05:33')
        self.assertEqual(type_change.to_string(time.localtime()), type_change.to_string(datetime.datetime.now()))
        self.assertEqual(type_change.to_string(datetime.time(12, 9, 2)), '12:09:02')

    def test_date_2_str(self):
        """date_2_str test"""
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
        """datetime_2_str test"""
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

    def test_time_functions(self):
        """all time functions test"""
        data = {'t1': datetime.datetime(2019, 7, 6, 8, 51, 6), 's1': '2019-07-29 15:03:8'}
        self.assertEqual(Interpreter.transform(data, 't1 $ toString'), '2019-07-06T08:51:06')
        self.assertEqual(Interpreter.transform(data, 't1 $ dateToString'), '2019-07-06')
        self.assertEqual(Interpreter.transform(data, 't1 $ datetimeToString'), '2019-07-06T08:51:06')
        self.assertEqual(Interpreter.transform(data, 's1 $ toDate'), datetime.date(2019, 7, 29))
        self.assertEqual(Interpreter.transform(data, 's1 $ toDatetime'), datetime.datetime(2019, 7, 29, 15, 3, 8))
        self.assertEqual(Interpreter.transform(data, 's1 $ dateToString'), '2019-07-29')

    def test_jtl(self):
        """jtl综合转换(无内嵌层)"""
        config_json = {
            "external_id": "user_id $ toString",
            "name": "name",
            "email": "email",
            "phone": "mobile_phone",
            "personal_id": "id_number",
            "age": "age",
            "gender": """gender $ enumChange '{"0": "女", "1": "男"}' """,
            "ethnicity": "nation",
            "nationality": "nationality",
            "year_of_work_experience": "work_year $ toInt",
            "birthday": {
                "_source_col_name": "birthday",
                "_type_change": "date_2_str",
                "format_str": "%Y/%m/%d"
            },
            "birthplace": "hometown",
            "marital_status": "marital_status $ enumFileChange 'tests/example_enum.json' ",
            "update_dt": {
                "_source_col_name": "update_dt",
                "_type_change": "datetime_2_str",
            },
            "update_dt2": "update_dt $ datetimeToString '%Y-%m-%dT%H:%M:%S' ",
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
                    "degree": """education $ enumChange '{"1": "高中及以下", "2": "大专", "3": "本科", "4": "硕士及以上"}' """,
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
                "_type_change": "jtl_change",
                "config_json": {
                    "school_name": "school_name",
                    "major": "major",
                    "degree": """education $ enumChange '{"1": "高中及以下", "2": "大专", "3": "本科", "4": "硕士及以上"}' """,
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
                        "_type_change": "jtl_change",
                        "config_json": {
                            "skill_category": "$ list skill_type compet_level time_use $ join '-' ",
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
                    'skill_category': '计算机水平考试一级证书-计算机水平一级',
                    'skill_name': '计算机水平考试一级证书',
                    'skill_level': '计算机水平一级'
                }, {
                    'skill_category': 'java-熟练',
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
        # print('*'*20)
        # print(type_change.jtl_change(db_data, config_json))
        # print(result)
        self.assertEqual(type_change.jtl_change(db_data, config_json), result)
        # 多检测一遍，确保输入数据源不会被修改
        self.assertEqual(type_change.jtl_change(db_data, config_json), result)


if __name__ == "__main__":
    unittest.main()
