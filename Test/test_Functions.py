# -*- coding:utf-8 -*-
"""
Functions unittest
"""

# Copyright (c) 2015-2019 Agalmic Ventures LLC (www.agalmicventures.com)
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

import uuid
import time
import datetime
import unittest

from JTL import Functions


class FunctionsTest(unittest.TestCase):

    def test_to_bool(self):
        self.assertEqual(Functions.to_bool('True'), True)
        self.assertEqual(Functions.to_bool('true'), True)

        self.assertEqual(Functions.to_bool('False'), False)
        self.assertEqual(Functions.to_bool('false'), False)

        self.assertEqual(Functions.to_bool('t'), False)
        self.assertEqual(Functions.to_bool('y'), False)

    def test_to_int(self):
        self.assertEqual(Functions.to_int('1'), 1)
        self.assertEqual(Functions.to_int('0'), 0)
        self.assertEqual(Functions.to_int('-1'), -1)

        self.assertEqual(Functions.to_int('1.1'), 1)
        self.assertEqual(Functions.to_int(1.1), 1)
        self.assertEqual(Functions.to_int('1.23e7'), 12300000)

    def test_to_float(self):
        self.assertEqual(Functions.to_float('1'), 1.0)
        self.assertEqual(Functions.to_float('0'), 0.0)
        self.assertEqual(Functions.to_float('-1'), -1.0)

        self.assertEqual(Functions.to_float('1.1'), 1.1)
        self.assertEqual(Functions.to_float(1.1), 1.1)
        self.assertEqual(Functions.to_float('1.23e7'), 12300000.0)

    def test_to_number(self):
        self.assertEqual(Functions.to_number('1'), 1)
        self.assertEqual(Functions.to_number('0'), 0)
        self.assertEqual(Functions.to_number('-1'), -1)

        self.assertEqual(Functions.to_number('1.1'), 1.1)
        self.assertEqual(Functions.to_number(1.1), 1.1)
        self.assertEqual(Functions.to_number('1.23e7'), 12300000.0)

    def test_to_string(self):
        self.assertEqual(Functions.to_string(None), None)
        self.assertEqual(Functions.to_string(''), '')
        self.assertEqual(Functions.to_string(b'aa'), 'aa')
        self.assertEqual(Functions.to_string(uuid.UUID('409c7441-a4a5-4ce1-9b3c-c7e0002e87bd')),
                         '409c7441a4a54ce19b3cc7e0002e87bd')

        # time
        self.assertEqual(Functions.to_string(datetime.datetime(2019, 9, 3, 8, 51, 6)), '2019-09-03T08:51:06')
        self.assertEqual(Functions.to_string(datetime.date(2019, 9, 13)), '2019-09-13')
        dt = time.strptime('2014/03/25 19:05:33', '%Y/%m/%d %H:%M:%S')
        self.assertEqual(Functions.to_string(dt), '2014-03-25T19:05:33')
        self.assertEqual(Functions.to_string(time.localtime()), Functions.to_string(datetime.datetime.now()))
        self.assertEqual(Functions.to_string(datetime.time(12, 9, 2)), '12:09:02')


if __name__ == "__main__":
    unittest.main()
