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

from JTL import Interpreter
from JTL import json_util, type_change


class InterpreterTest(unittest.TestCase):

    def setUp(self):
        self._testData = {
            'a': {
                'X': 3,
                'Y': 2
            },
            'b': {'p': {'d': {'q': 'test'}}},
            'c': 'asdf',
            'e': 'test馬大哈',
            'Z': '5.32e5'
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
        self.assertEqual(Interpreter.transform(self._testData, 'd $ or e a.Y False'), True)

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

        self.assertEqual(Interpreter.transform(self._testData, 'Z $ toInt'), 532000)
        self.assertEqual(Interpreter.transform(self._testData, 'Z $ toFloat $ + 1.2'), 532001.2)
        self.assertEqual(Interpreter.transform(self._testData, 'Z $ toNumber'), 532000)

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
        self.assertEqual(Interpreter.transform(self._testData, '''a.Y $ enumChange "{1: 'one', 2: 'two'}"'''), 'two')

    def test_transformSequence(self):
        self.assertEqual(Interpreter.transform(self._testData, '$ list a.X a.Y'), [3, 2])
        self.assertEqual(Interpreter.transform(self._testData, '* $ list a.X a.Y'), [3, 2])
        self.assertEqual(Interpreter.transform(self._testData, '$ list a.X a.Y $ 0'), 3)
        self.assertEqual(Interpreter.transform(self._testData, '$ list a.X a.Y $ first'), 3)
        self.assertEqual(Interpreter.transform(self._testData, '$ list a.X a.Y $ last'), 2)
        self.assertEqual(Interpreter.transform(self._testData, '$ list a.X a.Y 5 $ 2'), 5)
        self.assertEqual(Interpreter.transform(self._testData, '$ list a.X a.Y 5 $ 3'), None)
        self.assertEqual(Interpreter.transform(self._testData, '$ list a.X a.Y 0 $ rmFirst'), [2, 0])
        self.assertEqual(Interpreter.transform(self._testData, '$ list a.X a.Y 0 $ rmLast'), [3, 2])
        self.assertEqual(Interpreter.transform(self._testData, '$ list c b.p.d.q "h" $ join "-"'), 'asdf-test-h')
        self.assertEqual(Interpreter.transform(self._testData, '$ list c q "h" '), ['asdf', None, 'h'])
        self.assertEqual(Interpreter.transform(self._testData, '$ list c q "h" $ rmNull'), ['asdf', 'h'])

    def test_transformHash(self):
        self.assertEqual(Interpreter.transform(self._testData, 'c $ md5'), '912ec803b2ce49e4a541068d495ab570')
        self.assertEqual(Interpreter.transform(self._testData, 'e $ md5'), '61c78c5167f9b117b879def13b928bf3')
        self.assertEqual(Interpreter.transform(self._testData, 'c $ hmac_md5 Z'), '76e9d3d906862153da2406f38ea4b675')
        self.assertEqual(Interpreter.transform(self._testData, 'e $ hmac_md5 Z'), '9eb03ccdb4cf1920525210037a7bed58')
        self.assertEqual(Interpreter.transform(self._testData, 'c.d $ md5'), None)
        self.assertEqual(Interpreter.transform(self._testData, 'c $ sha1'), '3da541559918a808c2402bba5012f6c60b27661c')
        self.assertEqual(Interpreter.transform(self._testData, 'e $ sha1'), '06e92181a6fcbfc08396ea279340042b6e9edb4a')
        self.assertEqual(Interpreter.transform(self._testData, 'c $ hmac_sha1 Z'),
                         'e0ec9eb2b09a0346870c4c4d89a98f3046472720')
        self.assertEqual(Interpreter.transform(self._testData, 'e $ hmac_sha1 Z'),
                         '673670b77bc8a24709d227fb098614699507fa0e')

    def test_transformFunctions(self):
        transform_data = ('a $ keys $ sorted', lambda x, y: y.join(x), {'y': '**'})
        self.assertEqual(Interpreter.transformJson(self._testData, transform_data), 'X**Y')

        transform_data = ('a $ keys $ sorted', lambda x: ','.join(x))
        self.assertEqual(Interpreter.transformJson(self._testData, transform_data), 'X,Y')

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
