# -*- coding:utf-8 -*-

# Copyright (c) 2015-2020 Agalmic Ventures LLC (www.agalmicventures.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import binascii
import hashlib
import hmac
import math
from JTL import json_util


# ######### Basic Functions ##########


def to_bool(data):
    return data in (1, True, 'True', 'true')


def to_float(data):
    try:
        return float(data)
    except (ValueError, TypeError) as e:
        return None


def to_int(data):
    try:
        return int(data)
    except (ValueError, TypeError) as e:
        pass
    # 兼容 float 类型参数
    data = to_float(data)
    if data is None:
        return None
    try:
        return int(data)
    except (ValueError, TypeError) as e2:
        return None


def to_number(data):
    if isinstance(data, (int, float)):
        return data

    float_value = to_float(data)
    if float_value is not None:
        int_value = int(float_value)
        if float_value == int_value:
            return int_value
        return float_value

    return float_value


functions = {
    # Any
    'toBool': to_bool,
    'toFloat': to_float,
    'toInt': to_int,
    'toNumber': to_number,
    'null': lambda *args: None,

    # Bool
    'and': lambda *args: all(args),
    'or': lambda *args: any(args),

    # None
    'isNull': lambda x: x is None,

    'default': lambda x, y: x if x is not None else y,
    'defaultNan': lambda x: x if x is not None else float('nan'),

    # Sequence
    'first': lambda s: s[0] if s is not None and len(s) >= 1 else None,
    'last': lambda s: s[-1] if s is not None and len(s) >= 1 else None,
    'rmFirst': lambda s: s[1:] if s is not None and len(s) >= 1 else [],
    'rmLast': lambda s: s[:-1] if s is not None and len(s) >= 1 else [],
    'list': lambda x, *args: list(args),  # not include first element
    'rmNull': lambda args: [a for a in args if a is not None],

    # String
    'join': lambda s, sep='': sep.join(
        [functions.get('toString', str)(t) for t in s if t is not None]) if isinstance(s, (tuple, list)) else None,
}


# ######### Maybe Functions ##########

# Functions in here handle null like the Option type, if null in args return null
def maybe(f):
    return lambda *args: f(*args) if None not in args else None


# Functions that will be wrapped in maybe()
maybeFunctions = {
    # Bool
    'not': lambda x: not x,

    # Dict
    'keys': lambda d: list(d.keys()),
    'values': lambda d: list(d.values()),
    'enumChange': json_util.enum_change,
    'enumOrKey': json_util.enum_or_key,
    'enumFileChange': json_util.enum_file_change,

    # Number
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '**': lambda x, y: x ** y,
    '%': lambda x, y: x % y,

    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '<': lambda x, y: x < y,
    '<=': lambda x, y: x <= y,
    '>': lambda x, y: x > y,
    '>=': lambda x, y: x >= y,

    'isFinite': math.isfinite,
    'isNan': math.isnan,

    'abs': abs,
    'ceil': math.ceil,
    'cos': math.cos,
    'cosh': math.cosh,
    'erf': math.erf,
    'exp': math.exp,
    'floor': math.floor,
    'lg': math.log2,
    'ln': math.log,
    'log': math.log10,
    'sin': math.sin,
    'sinh': math.sinh,
    'sqrt': math.sqrt,
    'tan': math.tan,
    'tanh': math.tanh,

    # Sequence
    'count': lambda s, f: s.count(f),
    'length': len,
    'max': max,
    'min': min,
    'sorted': sorted,
    'sum': sum,
    'unique': lambda s: list(set(s)),

    # String
    'lower': lambda s: s.lower(),
    'upper': lambda s: s.upper(),
    'capitalize': lambda s: s.capitalize(),
    'swapCase': lambda s: s.swapcase(),

    'strip': lambda s: s.strip(),
    'lstrip': lambda s: s.lstrip(),
    'rstrip': lambda s: s.rstrip(),

    'find': lambda s, f: s.find(f),
    'replace': lambda s, f, g: s.replace(f, g),
    'startsWith': lambda s, f: s.startswith(f),
    'endsWith': lambda s, f: s.endswith(f),

    'split': lambda s, sp: s.split(sp),
    'lines': lambda s: s.split('\n'),
    'unlines': lambda s: '\n'.join(s),
    'words': lambda s: s.split(' '),
    'unwords': lambda s: ' '.join(s),
}

for name in maybeFunctions:
    function = maybeFunctions[name]
    functions[name] = maybe(function)


# ######### Hash Functions ##########

def hashFunction(hashConstructor):
    """
    Accepts the constructor of a hash algorithm and returns a function from a string to a hexified string digest.

    :param hashConstructor: hashing algorithm (e.g. hashlib.md5)
    :return: f(str)
    """

    def f(s):
        if s is None:
            return None
        h = hashConstructor()
        h.update(json_util.encode2bytes(s))
        return binascii.hexlify(h.digest()).decode('utf8')

    return f


def hmacFunction(hashConstructor):
    """
    Accepts the constructor of a hash algorithm and returns an HMAC function.

    :param hashConstructor: hashing algorithm (e.g. hashlib.md5)
    :return: hmac(str, key)
    """

    def h(message, key):
        key = json_util.encode2bytes(key)
        msg = json_util.encode2bytes(message)
        return hmac.new(key=key, msg=msg, digestmod=hashConstructor).hexdigest()

    return h


hashFunctions = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha224': hashlib.sha224,
    'sha256': hashlib.sha256,
    'sha384': hashlib.sha384,
    'sha512': hashlib.sha512,
}

for name in hashFunctions:
    function = hashFunctions[name]
    functions[name] = hashFunction(function)
    functions['hmac_%s' % name] = hmacFunction(function)


def register(operation, function):
    """add a function to JTL.
    :param operation: function name, the operation in JTL
    :param function: the function.
    """
    global functions
    functions[operation] = function


def register_maybe(operation, function):
    """add a maybe function to JTL.
    if null in args return null.
    :param operation: function name, the operation in JTL
    :param function: the function.
    """
    global functions
    functions[operation] = maybe(function)


def registerFunction(operation):
    """add a function to JTL.
    :param operation: function name, the operation in JTL
    """
    def wrap(function):
        global functions
        functions[operation] = function
        return function
    return wrap


def registerMaybeFunction(operation):
    """add a maybe function to JTL.
    if null in args return null.
    :param operation: function name, the operation in JTL
    """
    def wrap(function):
        global functions
        functions[operation] = maybe(function)
        return functions[operation]
    return wrap

