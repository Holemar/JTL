# -*- coding:utf-8 -*-

import re
import time
import datetime

__all__ = ('to_string', 'to_time', 'to_datetime', 'to_date', 'to_timestamp', 'to_datetime_time',
           'datetime_time_to_str', 'is_dst')

DEFAULT_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_MONTH_FORMAT = '%Y-%m'
DEFAULT_TIME_FORMAT = '%H:%M:%S'
FORMAT_LIST = (DEFAULT_FORMAT, '%Y-%m-%d %H:%M:%S.%f', DEFAULT_DATE_FORMAT, DEFAULT_MONTH_FORMAT, '%Y',
               '%Y年%m月%d日 %H时%M分%S秒', '%Y年%m月%d日　%H时%M分%S秒', '%Y年%m月%d日 %H时%M分', '%Y年%m月%d日　%H时%M分',
               '%Y年%m月%d日 %H:%M:%S', '%Y年%m月%d日　%H:%M:%S', '%Y年%m月%d日 %H:%M', '%Y年%m月%d日　%H:%M', '%Y年%m月%d日',
               '%Y/%m/%d %H:%M:%S', '%Y/%m/%d %H:%M:%S.%f', '%Y/%m/%d', '%Y%m%d', '%Y%m%d%H%M%S',
               '%Y/%m/%d %H:%M', '%Y-%m-%d %H:%M', "%Y-%m-%dT%H:%M",
               '%Y-%m-%d %p %I:%M:%S', '%Y-%m-%d %p %I:%M', '%Y/%m/%d %p %I:%M:%S', '%Y/%m/%d %p %I:%M',
               "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S+08:00", "%Y-%m-%dT%H:%M:%S.%f+08:00",
               )

# fix py3
try:
    long
except NameError:
    long = int
    basestring = str
    unicode = str

# hour,minute,second,microsecond format
time_re = re.compile(
    r'(?P<hour>\d{1,2}):(?P<minute>\d{1,2})'
    r'(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?'
)
# all time format
datetime_re = re.compile(
    r'(?P<year>\d{4})[-/](?P<month>\d{1,2})[-/](?P<day>\d{1,2})'
    r'([T ](?P<hour>\d{1,2}):(?P<minute>\d{1,2})'
    r'(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?'
    r'(?P<tzinfo>Z|[+-]\d{2}(?::?\d{2})?)?'
    r')?$'
)


def to_string(value=None, format_str=None, default_now=False):
    """
    change a time to str
    :param {time|datetime.datetime|datetime.date|int|long|float|string} value: original time
    :param {string} format_str: the return format of time. (default format: %Y-%m-%d %H:%M:%S)
    :param {bool} default_now: True: when value is None return now, False: when value is None return None.
    :return {string}: the string time
    """
    this_format = format_str
    if this_format is None:
        this_format = DEFAULT_FORMAT

    if value in (None, ''):
        if default_now is False:
            return None
        value = datetime.datetime.now()
        return value.strftime(this_format)
    # datetime
    elif isinstance(value, datetime.datetime):
        return value.strftime(this_format)
    # datetime.date
    elif isinstance(value, datetime.date):
        if format_str is None:
            this_format = DEFAULT_DATE_FORMAT
        return value.strftime(this_format)
    # time
    elif isinstance(value, time.struct_time):
        return time.strftime(this_format, value)
    # string, change type first
    elif isinstance(value, basestring):
        value = _str_2_datetime(value)
        return value.strftime(this_format)
    # number, treated as a timestamp
    elif isinstance(value, (int, long, float)):
        value = _number_2_datetime(value)
        return value.strftime(this_format)
    # datetime.timedelta, change type first
    elif isinstance(value, datetime.timedelta):
        value = _timedelta_2_datetime(value)
        return value.strftime(this_format)
    # datetime.time
    elif isinstance(value, datetime.time):
        if format_str is None:
            this_format = DEFAULT_TIME_FORMAT
        return value.strftime(this_format)
    return None


def to_time(value=None, default_now=False, from_format=None):
    """
    change other type of time to type(time)
    :param {time|datetime.datetime|datetime.date|int|long|float|string} value: time of other type
    :param {bool} default_now: True: when value is None return now, False: when value is None return None.
    :param {string} from_format: when input value is str, use this format to get time(default format: %Y-%m-%d %H:%M:%S)
    :return {time.struct_time}: the type(time) of time
    """
    if value in (None, ''):
        if default_now is False:
            return None
        return time.localtime()
    # datetime, datetime.date
    elif isinstance(value, (datetime.datetime, datetime.date)):
        return value.timetuple()
    # time
    elif isinstance(value, time.struct_time):
        return value
    # string, change type first
    elif isinstance(value, basestring):
        value = _str_2_datetime(value, from_format=from_format)
        return value.timetuple()
    # number, treated as a timestamp
    elif isinstance(value, (int, long, float)):
        return time.localtime(value)
    # datetime.timedelta, change type first
    elif isinstance(value, datetime.timedelta):
        value = _timedelta_2_datetime(value)
        return value.timetuple()
    return None


def to_datetime(value=None, default_now=False, from_format=None):
    """
    change other type of time to type(datetime.datetime)
    note: from type(time) to type(datetime.datetime), can not keep microsecond
    :param {time|datetime.datetime|datetime.date|int|long|float|string} value: time of other type
    :param {bool} default_now: True: when value is None return now, False: when value is None return None.
    :param {string} from_format: when input value is str, use this format to get time(default format: %Y-%m-%d %H:%M:%S)
    :return {datetime.datetime}: the type(datetime.datetime) of time
    """
    if value in (None, ''):
        if default_now is False:
            return None
        return datetime.datetime.now()
    # datetime
    elif isinstance(value, datetime.datetime):
        return value
    # datetime.date (different from datetime.datetime, it has not hour, minute and second)
    elif isinstance(value, datetime.date):
        return datetime.datetime(value.year, value.month, value.day)
        # return datetime.datetime.combine(value, datetime.datetime.min.time())
    # time
    elif isinstance(value, time.struct_time):
        return datetime.datetime(*value[:6])
    # string
    elif isinstance(value, basestring):
        return _str_2_datetime(value, from_format=from_format)
    # number, treated as a timestamp
    elif isinstance(value, (int, long, float)):
        return _number_2_datetime(value)
    # datetime.timedelta, change type first
    elif isinstance(value, datetime.timedelta):
        return _timedelta_2_datetime(value)
    return None


def to_date(value=None, default_now=False, from_format=None):
    """
    change other type of time to type(datetime.date)
    :param {time|datetime.datetime|datetime.date|int|long|float|string} value: time of other type
    :param {bool} default_now: True: when value is None return now, False: when value is None return None.
    :param {string} from_format: when input value is str, use this format to get time(default format: %Y-%m-%d %H:%M:%S)
    :return {datetime.date}: the type(datetime.date) of time
    """
    if value in (None, ''):
        if default_now is False:
            return None
        return datetime.date.today()
    # datetime
    elif isinstance(value, datetime.datetime):
        # return datetime.date(value.year, value.month, value.day)
        return value.date()
    # datetime.date, note: isinstance(datetime.datetime(), datetime.date) is True
    elif isinstance(value, datetime.date):
        return value
    # time
    elif isinstance(value, time.struct_time):
        return datetime.date(*value[:3])
    # string, change type first
    elif isinstance(value, basestring):
        value = _str_2_datetime(value, from_format=from_format)
        return value.date()
    # number, treated as a timestamp
    elif isinstance(value, (int, long, float)):
        return datetime.date.fromtimestamp(value)
    # datetime.timedelta, change type first
    elif isinstance(value, datetime.timedelta):
        value = _timedelta_2_datetime(value)
        return value.date()
    return None


def to_timestamp(value=None, from_format=None, default_now=False):
    """
    change time to timestamp(unit: second)
    :param {time|datetime.datetime|datetime.date|int|long|float|string} value: original time
    :param {bool} default_now: True: when value is None return now, False: when value is None return None.
    :param {string} from_format: when input value is str, use this format to get time(default format: %Y-%m-%d %H:%M:%S)
    :return {float}: timestamp(unit: second)
    """
    if value in (None, ''):
        if default_now is False:
            return None
        return time.time()
    # datetime, datetime.date
    elif isinstance(value, (datetime.datetime, datetime.date)):
        return time.mktime(value.timetuple())
    # time
    elif isinstance(value, time.struct_time):
        return time.mktime(value)
    # str
    elif isinstance(value, basestring):
        value = _str_2_datetime(value, from_format=from_format)
        return time.mktime(value.timetuple())
    # number, treated as a timestamp
    elif isinstance(value, (int, long, float)):
        return value
    # datetime.timedelta
    elif isinstance(value, datetime.timedelta):
        return value.days * 24 * 60 * 60 + value.seconds + (value.microseconds / 1000000.0)
    return None


def _str_2_datetime(value, from_format=None):
    """
    change string time to type(datetime.datetime)
    :param {string} value: original time
    :param {string} from_format: use this format to get time if has(default format: %Y-%m-%d %H:%M:%S)
    :return {datetime.datetime}: the type(datetime.datetime) of time
    """
    if from_format:
        return datetime.datetime.strptime(value, from_format)

    match = datetime_re.match(value)
    if match:
        kw = match.groupdict()
        if kw['microsecond']:
            kw['microsecond'] = kw['microsecond'].ljust(6, '0')
        kw.pop('tzinfo')  # utc not support
        kw = dict([(k, int(v)) for k, v in kw.items() if v is not None])
        return datetime.datetime(**kw)

    # try to fix Chinese
    global FORMAT_LIST
    if '上午' in value: value = value.replace('上午', 'AM')
    if u'上午' in value: value = value.replace(u'上午', 'AM')
    if '下午' in value: value = value.replace('下午', 'PM')
    if u'下午' in value: value = value.replace(u'下午', 'PM')
    for format in FORMAT_LIST:
        try:
            return datetime.datetime.strptime(value, format)
        except:
            pass

    raise ValueError("time data %r does not match time format" % value)


def _number_2_datetime(value):
    """
    number to time
    :param {int|long|float} value: timestamp
    :return {datetime.datetime}: time
    """
    return datetime.datetime.fromtimestamp(value)


def _timedelta_2_datetime(value):
    """
    datetime.timedelta to datetime.datetime
    :param {datetime.timedelta} value: time of type datetime.timedelta
    :return {datetime.datetime}: time of type datetime.datetime
    """
    return datetime.datetime.fromtimestamp(0) + value


def to_datetime_time(value):
    """
    change time to type of datetime.time
    :param {datetime.time|datetime.datetime|string} value: original time
    :return {datetime.time}: time of type datetime.time
    """
    if value in ('', None):
        return None
    if isinstance(value, basestring):
        match = time_re.match(value)
        if match:
            kw = match.groupdict()
            if kw['microsecond']:
                kw['microsecond'] = kw['microsecond'].ljust(6, '0')
            new_kw = {}
            for k, v in kw.items():
                if v is not None:
                    new_kw[k] = int(v)
            return datetime.time(**new_kw)
        else:
            value = to_datetime(value)
    # datetime.time
    if isinstance(value, datetime.time):
        return value
    # datetime.datetime
    elif isinstance(value, datetime.datetime):
        return datetime.time(value.hour, value.minute, value.second)
    # datetime.timedelta
    elif isinstance(value, datetime.timedelta):
        seconds = value.seconds
        hour = seconds // 3600
        minute = (seconds % 3600) // 60
        second = seconds % 60
        return datetime.time(hour, minute, second)
    return None


def datetime_time_to_str(value, format_str='%H:%M:%S'):
    """
    change time of type(datetime.time) to type(str)
    :param {datetime.time|string} value: original time
    :param {string} format_str: the return format of time. (default format: %H:%M:%S)
    :return {string}: the string time
    """
    value = to_datetime_time(value)
    if value is None:
        return None
    return value.strftime(format_str)


def is_dst(value=None, from_format=None):
    """
    whether daylight time
    :param {time|datetime.datetime|datetime.date|int|long|float|string} value: original time
    :param {string} from_format: when input value is str, use this format to get time(default format: %Y-%m-%d %H:%M:%S)
    :return {bool}: True when daylight time, else False
    """
    _time = to_time(value=value, from_format=from_format)
    return bool(_time.tm_isdst) if _time is not None else False
