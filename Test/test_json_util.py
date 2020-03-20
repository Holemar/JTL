# -*- coding:utf-8 -*-
"""
json Utility unittest
"""

import os
import uuid
import time
import decimal
import datetime
import unittest

from JTL import json_util


class TestJsonUtil(unittest.TestCase):

    def test_str_bytes(self):
        a = "哈哈xyz呵呵馬大親"
        s = json_util.decode2str(a)
        self.assertEqual(a, s)
        self.assertTrue(isinstance(s, str))

        c = b'absde'
        s2 = json_util.decode2str(c)
        self.assertTrue(isinstance(s2, str))
        self.assertEqual('absde', s2)

        b = json_util.encode2bytes(a)
        self.assertTrue(isinstance(b, bytes))
        d = json_util.encode2bytes(c)
        self.assertTrue(isinstance(d, bytes))
        self.assertEqual(c, d)

    def test_to_utf8_str(self):
        a = "哈哈xyz呵呵馬大親"
        for code in ('utf-8', 'GBK', 'big5', 'GB18030', 'unicode-escape'):
            # bytes
            b = bytes(a, code)
            s = json_util.to_utf8_str(b)
            self.assertTrue(isinstance(s, str))
            self.assertEqual(s, a)
            # bytearray
            br = bytearray(a, code)
            s = json_util.to_utf8_str(br)
            self.assertTrue(isinstance(s, str))
            self.assertEqual(s, a)

    def test_to_utf8_bytes(self):
        # big5
        a = "馬xyz大親"
        b0 = bytes(a, 'utf-8')
        code = 'big5'
        s0 = b0.decode(code)
        b2 = json_util.to_utf8_bytes(s0)
        self.assertTrue(isinstance(b2, bytes))
        self.assertEqual(b2, b0)
        # str
        s = json_util.to_utf8_str(s0)
        self.assertTrue(isinstance(s, str))
        self.assertEqual(s, a)

        a = "哈哈xyz呵呵大的"
        b0 = bytes(a, 'utf-8')
        for code in ('utf-8', 'gbk', 'GB18030', 'unicode-escape'):
            s0 = b0.decode(code)
            b2 = json_util.to_utf8_bytes(s0)
            self.assertTrue(isinstance(b2, bytes))
            self.assertEqual(b2, b0)
            # str
            s = json_util.to_utf8_str(s0)
            self.assertTrue(isinstance(s, str))
            self.assertEqual(s, a)

    def test_base64(self):
        a = "W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0="
        ra = '[[], {}, {"callbacks": null, "errbacks": null, "chain": null, "chord": null}]'
        self.assertEqual(json_util.base64_decode(a), ra)
        self.assertEqual(json_util.base64_encode(ra), a)

    def test_enum_file_change(self):
        """enum_file_change test"""
        file_name = '_example_enum.json'
        content = '''{ "0": "未婚", "1": "已婚", "2": "离异", 4: "丧偶",}'''
        with open(os.path.join(os.getcwd(), file_name), 'w', encoding='utf-8') as file:
            file.write(content)

        self.assertEqual(json_util.enum_file_change('2', file_name), '离异')
        self.assertEqual(len(json_util.BIG_ENUM_JSON), 1)
        enum_dict = json_util.BIG_ENUM_JSON.get(file_name)
        self.assertEqual(enum_dict.get(1), None)

        self.assertEqual(json_util.enum_file_change(1, file_name), '已婚')
        self.assertEqual(len(json_util.BIG_ENUM_JSON), 1)
        enum_dict2 = json_util.BIG_ENUM_JSON.get(file_name)
        self.assertEqual(id(enum_dict), id(enum_dict2))
        self.assertEqual(enum_dict2.get(1), '已婚')

        self.assertEqual(enum_dict.get("未婚"), None)
        self.assertEqual(json_util.enum_file_change("未婚", file_name), "未婚")
        enum_dict2 = json_util.BIG_ENUM_JSON.get(file_name)
        self.assertEqual(id(enum_dict), id(enum_dict2))
        self.assertEqual(enum_dict2.get("未婚"), "未婚")

        self.assertEqual(json_util.enum_file_change("4", file_name), "丧偶")
        self.assertEqual(json_util.enum_file_change(5, file_name), None)
        self.assertEqual(json_util.enum_file_change('10', file_name), None)
        os.remove(file_name)

    def test_enum_change(self):
        """enum_change tests"""
        self.assertEqual(json_util.enum_change(1, "{1: '一', 2: '二', 3: '三'}"), '一')
        self.assertEqual(json_util.enum_change(1, {1: '一', 2: '二', 3: '三'}), '一')
        self.assertEqual(json_util.enum_change('3', {1: '一', 2: '二', 3: '三'}), '三')
        self.assertEqual(json_util.enum_change(1, {'1': '一', '2': '二', '3': '三'}), '一')
        self.assertEqual(json_util.enum_change('2', {'1': '一', '2': '二', '3': '三'}), '二')
        self.assertEqual(json_util.enum_change('二', {1: '一', 2: '二', 3: '三'}), '二')
        self.assertEqual(json_util.enum_change(5, {'1': '一', '2': '二', '3': '三'}), None)
        self.assertEqual(json_util.enum_change('10', {'1': '一', '2': '二', '3': '三'}), None)

    def test_enum_or_key(self):
        """enum_or_key tests"""
        self.assertEqual(json_util.enum_or_key(1, "{1: '一', 2: '二', 3: '三'}"), '一')
        self.assertEqual(json_util.enum_or_key(1, {1: '一', 2: '二', 3: '三'}), '一')
        self.assertEqual(json_util.enum_or_key('3', {1: '一', 2: '二', 3: '三'}), '三')
        self.assertEqual(json_util.enum_or_key(1, {'1': '一', '2': '二', '3': '三'}), '一')
        self.assertEqual(json_util.enum_or_key('2', {'1': '一', '2': '二', '3': '三'}), '二')
        self.assertEqual(json_util.enum_or_key('二', {1: '一', 2: '二', 3: '三'}), '二')
        self.assertEqual(json_util.enum_or_key(5, {'1': '一', '2': '二', '3': '三'}), 5)
        self.assertEqual(json_util.enum_or_key('10', {'1': '一', '2': '二', '3': '三'}), '10')

    def test_load_json(self):
        """load_json test"""
        self.assertEqual(json_util.load_json('{"哈":11.2, "aa":[1,"2",3]}'), {u"哈": 11.2, "aa": [1, "2", 3]})
        self.assertEqual(json_util.load_json('{"n":null, "aa":[true,"2",false]}'),
                         {"n": None, "aa": [True, "2", False]})
        self.assertEqual(json_util.load_json('{"n":None, "aa":[True,"2",False,]}'),
                         {"n": None, "aa": [True, "2", False]})

    def test_load_json_file(self):
        """load_json_file 测试"""

        file_name = os.path.join(os.getcwd(), 'tests/_test.json')
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('{"哈":11.2, "aa":[1,"2",3]}')
        self.assertEqual(json_util.load_json_file(file_name), {u"哈": 11.2, "aa": [1, "2", 3]})

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('{"n":null, "aa":[true,"2",false]}')
        self.assertEqual(json_util.load_json_file(file_name), {"n": None, "aa": [True, "2", False]})

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('{"n":None, "aa":[True,"2",False,]}')
        self.assertEqual(json_util.load_json_file(file_name), {"n": None, "aa": [True, "2", False]})

        os.remove(file_name)

    def test_load_dump_json_file(self):
        """load_json_file test"""

        file_name = os.path.join(os.getcwd(), 'tests/_test2.json')
        t = {u"哈": 11.2, "aa": [1, "2", 3]}
        json_util.dump_json_file(t, file_name)
        self.assertEqual(json_util.load_json_file(file_name), t)

        t = {"n": None, "aa": [True, "2", False]}
        json_util.dump_json_file(t, file_name)
        self.assertEqual(json_util.load_json_file(file_name), t)

        t = {"n": None, "aa": [True, "2", False], u"可": "呵呵!@#$%^&*()_+"}
        json_util.dump_json_file(t, file_name)
        self.assertEqual(json_util.load_json_file(file_name), t)

        t = {'aa': 4.55, 'b1': {'ll': 66.55, u'测试': 554, '测试2': u'测试2值', 'c': [1, u'哈啊', '啊哈']},
                u'元组': (set('abcd'), decimal.Decimal('55.6722'), datetime.datetime(2015, 6, 28, 14, 19, 41)),
                datetime.date(2019, 6, 18): uuid.UUID('81ab20bf-ecd9-4cc7-beb1-498da7e0b75d')}
        json_util.dump_json_file(t, file_name)
        t2 = {'aa': 4.55, 'b1': {'ll': 66.55, '测试': 554, '测试2': '测试2值', 'c': [1, '哈啊', '啊哈']},
             '元组': [list(set('abcd')), 55.6722, '2015-06-28T14:19:41'],
             '2019-06-18': '81ab20bfecd94cc7beb1498da7e0b75d'}
        self.assertEqual(json_util.load_json_file(file_name), t2)

        os.remove(file_name)

    def test_json_serializable(self):
        """json_serializable test"""
        # None,bool,int,float serializable
        self.assertEqual(json_util.json_serializable([None, '', True, False, 1122, 33.054]),
                         [None, '', True, False, 1122, 33.054])

        # key, uuid, datetime serializable
        self.assertEqual(json_util.json_serializable(
            {uuid.UUID('81ab20bf-ecd9-4cc7-beb1-498da7e0b75d'): datetime.datetime(2015, 6, 28, 14, 19, 41)}),
            {'81ab20bfecd94cc7beb1498da7e0b75d': '2015-06-28T14:19:41'})

        # tuple, set, decimal serializable
        self.assertEqual(json_util.json_serializable(
            (set('abcd'), decimal.Decimal('55.6722'), datetime.date(2019, 6, 18), time.localtime())),
            [list(set('abcd')), 55.6722, '2019-06-18', time.strftime('%Y-%m-%dT%H:%M:%S')])

        # all
        arg1 = {'aa': 4.55, 'b1': {'ll': 66.55, u'测试': 554, '测试2': u'测试2值', 'c': [1, u'哈啊', '啊哈']},
                u'元组': (set('abcd'), decimal.Decimal('55.6722'), datetime.datetime(2015, 6, 28, 14, 19, 41)),
                datetime.date(2019, 6, 18): uuid.UUID('81ab20bf-ecd9-4cc7-beb1-498da7e0b75d')}
        self.assertEqual(json_util.json_serializable(arg1),
            {'aa': 4.55, 'b1': {'ll': 66.55, '测试': 554, '测试2': '测试2值', 'c': [1, '哈啊', '啊哈']},
             '元组': [list(set('abcd')), 55.6722, '2015-06-28T14:19:41'],
             '2019-06-18': '81ab20bfecd94cc7beb1498da7e0b75d'})


if __name__ == "__main__":
    unittest.main()
