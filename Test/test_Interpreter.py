# -*- coding:utf-8 -*-
"""
Interpreter unittest
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

import unittest

from JTL import Interpreter, json_util


class InterpreterTest(unittest.TestCase):

    def setUp(self):
        self._testData = {
            'a': {
                'X': 3,
                'Y': 2,
            },
            'b': {'p': {'d': {'q': 'test'}}},
            'c': 'asdf',
        }

    def test_transformChain(self):
        self.assertEqual(Interpreter.transform(self._testData, 'a.X'), 3)
        self.assertEqual(Interpreter.transform(self._testData, 'a $ .X'), 3)
        self.assertEqual(Interpreter.transform(self._testData, 'a $ .X $ toString'), "3")

    def test_transformBool(self):
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ not'), False)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ and a.Y'), True)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ and a.Y c'), True)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ and false'), False)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ and a.Y d'), False)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ or False'), True)

    def test_transformArithmetic(self):
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ + a.Y'), 5)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ + 66'), 69)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ - a.Y'), 1)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ * a.Y'), 6)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ * 2.5'), 7.5)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ * "a"'), 'aaa')
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ / a.Y'), 1.5)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ % a.Y'), 1)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ ** a.Y'), 9)

    def test_transformComparison(self):
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ == 3'), True)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ != 3'), False)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ >= 3'), True)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ > 3'), False)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ <= 3'), True)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ < 3'), False)
        self.assertEqual(Interpreter.transform(self._testData, 'a.X $ == 3 $ not'), False)

    def test_transformDictionary(self):
        self.assertEqual(Interpreter.transform(self._testData, 'a $ keys $ sorted'), ['X', 'Y'])
        self.assertEqual(Interpreter.transform(self._testData, 'a $ values $ sorted'), [2, 3])
        self.assertEqual(Interpreter.transform(self._testData, '$ list a.X a.Y'), [3, 2])
        self.assertEqual(Interpreter.transform(self._testData, '* $ list a.X a.Y'), [3, 2])
        self.assertEqual(Interpreter.transform(self._testData, '$ list a.X a.Y $ 0'), 3)
        self.assertEqual(Interpreter.transform(self._testData, '$ list a.X a.Y $ first'), 3)
        self.assertEqual(Interpreter.transform(self._testData, '$ list a.X a.Y 5 $ 2'), 5)
        self.assertEqual(Interpreter.transform(self._testData, '$ list a.X a.Y 5 $ 3'), None)
        self.assertEqual(Interpreter.transform(self._testData, '$ list c b.p.d.q "h" $ join "-"'), 'asdf-test-h')

    def test_transformJson(self):
        for test_name in ["faa1", "test1"]:
            _json = json_util.load_json_file('tests/%s.json' % test_name)
            _config = json_util.load_json_file('tests/%s.jtl' % test_name)
            _result = json_util.load_json_file('tests/%s.result' % test_name)
            self.assertIsNotNone(_json)
            self.assertIsNotNone(_config)
            self.assertIsNotNone(_result)
            self.assertEqual(Interpreter.transformJson(_json, _config), _result)

    def test_my(self):
        data = {
            "weather": {
                "temp": "66.0 F (18.9 C)",
            },
            'gender': 1,
            'list': ['aa', 'bb', 'ccc']
        }
        self.assertEqual(Interpreter.transformJson(data, {"tempF": "weather.temp"}), {'tempF': "66.0 F (18.9 C)"})
        self.assertEqual(Interpreter.transformJson(data, {"tempF": "weather.temp$words"}),
                         {'tempF': ['66.0', 'F', '(18.9', 'C)']})
        self.assertEqual(Interpreter.transformJson(data, {"tempF": "weather.temp$words$first"}), {'tempF': '66.0'})
        self.assertEqual(Interpreter.transformJson(data, {"tempF": "weather.temp $ words $ first $ toFloat"}),
                         {'tempF': 66.0})
        self.assertEqual(Interpreter.transformJson(data, {"tempF": "weather.temp $ words $ first $ toFloat $ + 33.5"}),
                         {'tempF': 99.5})
        self.assertEqual(Interpreter.transformJson(data, {"weatherF": {"tempF": "weather.temp"}, 'gender': 1}),
                         {'weatherF': {'tempF': '66.0 F (18.9 C)'}, 'gender': 1})
        self.assertEqual(Interpreter.transformJson(data, {"tempF": "*"}), {'tempF': data})
        self.assertEqual(Interpreter.transformJson(data, {"tempF": "weather.temp2"}), {'tempF': None})
        self.assertEqual(Interpreter.transformJson(data, {"tempF": "list $ 2"}), {'tempF': 'ccc'})
        self.assertEqual(Interpreter.transformJson(data, {"tempF": "list $ 5"}), {'tempF': None})
        self.assertEqual(Interpreter.transformJson(data, {"tempF": "list $ join '-'"}), {'tempF': 'aa-bb-ccc'})
        self.assertEqual(Interpreter.transformJson(data, {"tempF": """not_name $ default "aaa" """}), {'tempF': 'aaa'})
        self.assertEqual(Interpreter.transformJson(data, {"tempF": "not_name $ default 'aaa'"}), {'tempF': 'aaa'})
        self.assertEqual(Interpreter.transformJson(data, {"tempF": """not_name $ default "{'a': 22}" """}),
                         {'tempF': "{'a': 22}"})


if __name__ == "__main__":
    unittest.main()
