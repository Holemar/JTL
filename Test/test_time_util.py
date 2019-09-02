#!python
# -*- coding:utf-8 -*-

import time
from datetime import datetime, date, timedelta, time as dt
import calendar
import unittest

from JTL.time_util import *

now = lambda: datetime.now().replace(microsecond=0)


def _sub_dict(**kwargs):
    zero_secends = {'years': 0, 'months': 0, 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'sum_days': 0,
                    'sum_seconds': 0}
    zero_secends.update(kwargs)
    return zero_secends


class TimeUtilTest(unittest.TestCase):

    def test_to_string(self):
        now_str = lambda: now().strftime('%Y-%m-%d %H:%M:%S')
        # 测试默认值及当前时间
        self.assertEqual(to_string(), None)
        self.assertEqual(to_string(default_now=True), now_str())  # 默认返回当前时间
        self.assertEqual(to_string(None), None)  # 默认返回当前时间
        self.assertEqual(to_string(None, default_now=True), now_str())  # 默认返回当前时间
        self.assertEqual(to_string(''), None)
        self.assertEqual(to_string('', default_now=True), now_str())  # 默认返回当前时间
        self.assertEqual(to_string(time.time()), now_str())  # 时间戳
        self.assertEqual(to_string(0), to_string(time.localtime(0)))  # 时间戳为0时
        # timedelta 类型
        self.assertEqual(to_string(timedelta()), to_string(0))
        self.assertEqual(to_string(timedelta(0, 3602)), to_string(3602))
        self.assertEqual(to_string(timedelta(5, 3602)), to_string(5 * 24 * 3600 + 3602))
        # 多种格式的日期格式
        self.assertEqual(to_string('2014-02-06 08:51:06'), '2014-02-06 08:51:06')  # 字符串
        self.assertEqual(to_string('2014-2-6 8:51:06'), '2014-02-06 08:51:06')  # 字符串
        self.assertEqual(to_string('2014/02/06'), '2014-02-06 00:00:00')  # 字符串
        self.assertEqual(to_string('2014/2/6 23:59:59'), '2014-02-06 23:59:59')  # 字符串
        self.assertEqual(to_string('2014/2/6 23:59'), '2014-02-06 23:59:00')  # 字符串
        self.assertEqual(to_string('2014-2-06 23:59'), '2014-02-06 23:59:00')  # 字符串
        self.assertEqual(to_string('2014年2月6日 23:59'), '2014-02-06 23:59:00')  # 字符串
        self.assertEqual(to_string('2014年2月6日 23时59分'), '2014-02-06 23:59:00')  # 字符串
        self.assertEqual(to_string('2014年02月6日 23时59分0秒'), '2014-02-06 23:59:00')  # 字符串
        self.assertEqual(to_string('2014年2月06日 23:59:00'), '2014-02-06 23:59:00')  # 字符串
        self.assertEqual(to_string('2014-2-6T23:59'), '2014-02-06 23:59:00')  # 字符串
        self.assertEqual(to_string('2014-2-6T23:59:00'), '2014-02-06 23:59:00')  # 字符串
        self.assertEqual(to_string('1900-1-1'), '1900-01-01 00:00:00')  # 字符串
        self.assertEqual(to_string('197011'), '1970-01-01 00:00:00')  # 字符串
        self.assertEqual(to_string('197011810'), '1970-01-01 08:01:00')  # 字符串
        self.assertEqual(to_string('2014-2-6 下午 11:59:00'), '2014-02-06 23:59:00')  # 字符串
        self.assertEqual(to_string('2014-2-6 下午 11:59'), '2014-02-06 23:59:00')  # 字符串
        self.assertEqual(to_string('2014-2-6 PM 11:59:00'), '2014-02-06 23:59:00')  # 字符串
        self.assertEqual(to_string('2014-2-6 PM 11:59'), '2014-02-06 23:59:00')  # 字符串
        self.assertEqual(to_string('2014/02/06 下午 11:59'), '2014-02-06 23:59:00')  # 字符串
        self.assertEqual(to_string('2014/02/06 PM 11:59:00'), '2014-02-06 23:59:00')  # 字符串

        # self.assertEqual(to_string('2014-02/06 08:51:06'), '2014-02-06 08:51:06' # 字符串(这本应是错误格式)
        # 不同类型的参数
        test_time = datetime(2014, 2, 6, 8, 51, 6)
        self.assertEqual(to_string(test_time), '2014-02-06 08:51:06')  # datetime
        self.assertEqual(to_string(time.strptime('2014/03/25 19:05:33', '%Y/%m/%d %H:%M:%S')),
                         '2014-03-25 19:05:33')  # time
        self.assertEqual(to_string(date.today()), now().strftime('%Y-%m-%d'))  # date
        # 指定格式化输出
        self.assertEqual(to_string(test_time, '%Y/%m/%dxx'), '2014/02/06xx')
        self.assertEqual(to_string(test_time, '%Y-%m/%dxx%H+%M+%S'), '2014-02/06xx08+51+06')
        self.assertEqual(to_string('2014-02-06 08:51:06', '%Y/%m/%d %H:%Mxx'), '2014/02/06 08:51xx')

    def fun_test(self, fun, default_time, test_time, test_date):
        # 测试默认值及当前时间
        self.assertEqual(fun(), None)
        self.assertEqual(fun(default_now=True), default_time())  # 默认返回当前时间
        self.assertEqual(fun(None), None)
        self.assertEqual(fun(None, default_now=True), default_time())  # 默认返回当前时间
        self.assertEqual(fun(''), None)
        self.assertEqual(fun('', default_now=True), default_time())  # 默认返回当前时间
        self.assertEqual(fun(time.time()), default_time())  # 时间戳
        self.assertEqual(fun(0), fun(time.localtime(0)))  # 时间戳为0时
        self.assertEqual(fun(0, default_now=True), fun(time.localtime(0)))  # 时间戳为0时
        # 测试指定时间
        self.assertEqual(fun('2014-02-06 08:51:06'), test_time)  # 字符串
        self.assertEqual(fun('2014/02-6 8xx51mm06::YY', '%Y/%m-%d %Hxx%Mmm%S::YY'), test_time)  # 格式化测试
        self.assertEqual(fun(datetime(2014, 2, 6, 8, 51, 6)), test_time)  # datetime
        self.assertEqual(fun(time.strptime('2014-02-06 08:51:06', '%Y-%m-%d %H:%M:%S')), test_time)  # time
        self.assertEqual(fun(date(2014, 2, 6)), test_date)  # date
        # 多种格式的日期格式
        self.assertEqual(fun('2014/02/06 08:51:06'), test_time)
        self.assertEqual(fun('20142685106'), test_time)
        self.assertEqual(fun('2014268516'), test_time)
        self.assertEqual(fun('2014/2/6 8:51:6'), test_time)
        self.assertEqual(fun('2014/2/06 08:51:6'), test_time)
        self.assertEqual(fun('2014-02-06T08:51:06'), test_time)
        self.assertEqual(fun('2014-02-06T08:51:06+08:00'), test_time)
        self.assertEqual(fun('2014-02-06T08:51:06.000Z'), test_time)
        self.assertEqual(fun('2014-02-06 AM 08:51:06'), test_time)
        self.assertEqual(fun('2014-02-06 上午 08:51:06'), test_time)
        self.assertEqual(fun(u'2014-02-06 上午 08:51:06'), test_time)
        self.assertEqual(fun('2014/2/06 AM 08:51:06'), test_time)
        self.assertEqual(fun('2014/02/06 上午 08:51:06'), test_time)
        # 测试日期
        self.assertEqual(fun('2014-02-06'), test_date)
        self.assertEqual(fun('2014-2-6'), test_date)
        self.assertEqual(fun('2014/02/06'), test_date)
        self.assertEqual(fun('2014/2/6'), test_date)
        self.assertEqual(fun('201426'), test_date)
        # timedelta 类型
        if fun == to_time:
            self.assertEqual(fun(timedelta())[:6], fun(0)[:6])
            self.assertEqual(fun(timedelta(0, 3602))[:6], fun(3602)[:6])
            self.assertEqual(fun(timedelta(5, 3602))[:6], fun(5 * 24 * 3600 + 3602)[:6])
        else:
            self.assertEqual(fun(timedelta()), fun(0))
            self.assertEqual(fun(timedelta(0, 3602)), fun(3602))
            self.assertEqual(fun(timedelta(5, 3602)), fun(5 * 24 * 3600 + 3602))

    # to_time 测试
    def test_to_time(self):
        now_time = time.localtime
        test_time = time.strptime('2014-02-06 08:51:06', '%Y-%m-%d %H:%M:%S')  # 测试时间
        test_date = time.strptime('2014-02-06', '%Y-%m-%d')  # 测试日期
        self.fun_test(to_time, now_time, test_time, test_date)

    def my_to_datetime(self, *args, **kwargs):
        res = to_datetime(*args, **kwargs)
        res = res.replace(microsecond=0) if res else res  # 忽略微秒数
        return res

    # to_datetime 测试
    def test_to_datetime(self):
        test_time = datetime(2014, 2, 6, 8, 51, 6)  # 测试时间
        test_date = datetime(2014, 2, 6)  # 测试日期
        self.fun_test(self.my_to_datetime, now, test_time, test_date)

    # to_date 测试
    def test_to_date(self):
        now_time = date.today
        test_time = date(2014, 2, 6)  # 测试时间
        test_date = date(2014, 2, 6)  # 测试日期
        self.fun_test(to_date, now_time, test_time, test_date)

    def my_to_timestamp(self, *args, **kwargs):
        res = to_timestamp(*args, **kwargs)
        res = int(res) if res else res  # 忽略微秒数
        return res

    # to_timestamp 测试
    def test_to_timestamp(self):
        now_time = lambda: int(time.time())
        test_time = time.mktime(time.strptime('2014-02-06 08:51:06', '%Y-%m-%d %H:%M:%S'))  # 测试时间
        test_date = time.mktime(time.strptime('2014-02-06', '%Y-%m-%d'))  # 测试日期
        self.fun_test(self.my_to_timestamp, now_time, test_time, test_date)

    # to_datetime_time 测试
    def test_to_datetime_time(self):
        test_time = dt(12, 9, 2)
        self.assertEqual(to_datetime_time("12:9:2"), test_time)
        self.assertEqual(to_datetime_time("12:09:02"), test_time)
        self.assertEqual(to_datetime_time(test_time), test_time)
        self.assertEqual(to_datetime_time('0:0:0'), dt())
        self.assertEqual(to_datetime_time(datetime(2017, 9, 5, 15, 53, 2)), dt(15, 53, 2))
        # 没有秒
        test_time2 = dt(12, 9)
        self.assertEqual(to_datetime_time("12:9"), test_time2)
        self.assertEqual(to_datetime_time("12:09:00"), test_time2)
        self.assertEqual(to_datetime_time("12:9:0"), test_time2)
        self.assertEqual(to_datetime_time('0:0'), dt())
        # 错误类型
        self.assertEqual(to_datetime_time(None), None)
        self.assertEqual(to_datetime_time(''), None)
        self.assertEqual(to_datetime_time(12345), None)
        # self.assertEqual(to_datetime_time("2014-02-06 12:09:00"), None
        # datetime 类型字符串
        self.assertEqual(to_datetime_time('2014-02-06 08:51:06'), dt(8, 51, 6))
        self.assertEqual(to_datetime_time('2014/02/06'), dt(0, 0, 0))
        self.assertEqual(to_datetime_time('2014/2/6 23:59:59'), dt(23, 59, 59))
        self.assertEqual(to_datetime_time('2014/2/6 23:59'), dt(23, 59, 0))
        self.assertEqual(to_datetime_time('2014-2-06 23:59'), dt(23, 59, 0))
        self.assertEqual(to_datetime_time('2014年2月6日 23:59'), dt(23, 59, 0))
        self.assertEqual(to_datetime_time('2014年2月6日 23时59分'), dt(23, 59, 0))
        self.assertEqual(to_datetime_time('2014年02月6日 23时59分0秒'), dt(23, 59, 0))
        self.assertEqual(to_datetime_time('2014年2月06日 23:59:00'), dt(23, 59, 0))
        self.assertEqual(to_datetime_time('1900-1-1'), dt(0, 0, 0))
        self.assertEqual(to_datetime_time('197011'), dt(0, 0, 0))
        self.assertEqual(to_datetime_time('197011810'), dt(8, 1, 0))
        # timedelta 类型
        self.assertEqual(to_datetime_time(timedelta()), dt(0, 0, 0))
        self.assertEqual(to_datetime_time(timedelta(0, 3602)), dt(1, 0, 2))
        self.assertEqual(to_datetime_time(timedelta(5, 3602)), dt(1, 0, 2))

    # datetime_time_to_str 测试
    def test_datetime_time_to_str(self):
        test_time = dt(12, 9, 2)
        self.assertEqual(datetime_time_to_str(test_time), "12:09:02")
        self.assertEqual(datetime_time_to_str(test_time, '%H:%M'), "12:09")
        self.assertEqual(datetime_time_to_str("12:9"), "12:09:00")
        self.assertEqual(datetime_time_to_str("12:9:2"), "12:09:02")
        self.assertEqual(datetime_time_to_str(dt()), "00:00:00")
        self.assertEqual(datetime_time_to_str('0:0:0'), "00:00:00")
        self.assertEqual(datetime_time_to_str('0:0'), "00:00:00")
        # 错误类型
        self.assertEqual(datetime_time_to_str(None), None)
        self.assertEqual(datetime_time_to_str(''), None)
        self.assertEqual(datetime_time_to_str(12345), None)
        self.assertEqual(datetime_time_to_str("2014-02-06 12:09:00"), "12:09:00")
        # timedelta 类型
        self.assertEqual(datetime_time_to_str(timedelta()), "00:00:00")
        self.assertEqual(datetime_time_to_str(timedelta(0, 3602)), "01:00:02")
        self.assertEqual(datetime_time_to_str(timedelta(5, 3602)), "01:00:02")
        self.assertEqual(datetime_time_to_str(timedelta(0, -2)), "23:59:58")


if __name__ == "__main__":
    unittest.main()
